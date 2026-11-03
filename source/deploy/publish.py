"""Publish the already staged artifact through the existing Nginx vhost, with rollback."""
from pathlib import Path
import hashlib,json,signal,subprocess,time
import requests

ROOT=Path(__file__).resolve().parents[1]
CONFIG=Path('/etc/nginx/sites-available/korvuz.site')

def run(*args):
    return subprocess.run(args,check=True)

def read_private(path):
    return subprocess.check_output(['sudo','-n','cat',str(path)])

def interrupted(signum,frame):
    raise RuntimeError('Deployment interrupted; restoring previous configuration')

def main():
    release=json.loads((ROOT/'deploy/release.json').read_text())
    backup=Path(release['backup'])
    assert backup.parent==Path('/opt/korvuz-backups') and backup.name not in ('','.','..')
    assert Path(release['root']).parent==Path('/opt/korvuz-releases')
    point=json.loads(read_private(backup/'rollback-point.json'))
    previous=read_private(backup/'nginx.previous.conf')
    assert CONFIG.read_bytes()==previous,'Production config changed after backup; stop'
    response=requests.get(release['url'],timeout=20);response.raise_for_status()
    assert hashlib.sha256(response.content).hexdigest()==point['live_index_sha256'],'Production changed after backup; stop'
    manifest=(ROOT/'dist/release-manifest.json').read_bytes()
    assert hashlib.sha256(manifest).hexdigest()==release['manifest_sha256']
    assert (Path(release['root'])/'release-manifest.json').read_bytes()==manifest
    inventory=json.loads(manifest)
    for name,digest in inventory.items():
        file=Path(release['root'])/name
        assert file.resolve().is_relative_to(Path(release['root']).resolve())
        assert hashlib.sha256(file.read_bytes()).hexdigest()==digest,name
    preflight=json.loads((ROOT/'test-results/deploy-preflight/smoke.json').read_text())
    assert preflight['passed'] and preflight['version']==release['manifest_sha256']
    changed=False
    signal.signal(signal.SIGTERM,interrupted)
    signal.signal(signal.SIGINT,interrupted)
    try:
        run('sudo','-n','install','-o','root','-g','root','-m','644',str(ROOT/'deploy/korvuz.site.conf'),str(CONFIG)+'.pending')
        changed=True
        run('sudo','-n','mv','-T',str(CONFIG)+'.pending',str(CONFIG))
        run('sudo','-n','nginx','-t')
        run('sudo','-n','systemctl','reload','nginx')
        for attempt in range(20):
            response=requests.get(release['url']+'release-manifest.json',timeout=10)
            if response.status_code==200 and response.content==manifest:break
            time.sleep(.5)
        else:raise RuntimeError('Public host did not activate the approved release')
        result=subprocess.run(['node','deploy/smoke.mjs',release['url'],'test-results/deploy-live'],cwd=ROOT,start_new_session=True,timeout=600)
        if result.returncode:raise RuntimeError('Live smoke failed; rolling back')
        release['status']='deployed-and-live-smoke-passed'
        (ROOT/'deploy/deployment-result.json').write_text(json.dumps(release,indent=2)+'\n')
        print('DEPLOYED',release['version'],release['url'],flush=True)
    except BaseException:
        if changed:
            run('sudo','-n','sh',str(backup/'rollback.sh'),str(backup))
            for attempt in range(20):
                old=requests.get(release['url'],timeout=10)
                if hashlib.sha256(old.content).hexdigest()==point['live_index_sha256']:break
                time.sleep(.5)
            else:raise RuntimeError('Rollback verification failed; immediate operator action required')
            print('ROLLED BACK: previous public homepage verified',flush=True)
        raise

if __name__=='__main__':main()
