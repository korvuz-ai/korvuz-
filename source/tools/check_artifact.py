"""Local link, asset, schema and preservation checks for the static release."""
from pathlib import Path
import sys
if __package__ in (None,''):sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse,json,hashlib,gzip,re
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup

def check_artifact(root:Path,baseline:Path)->list[str]:
    errors=[];baseline_data=json.loads(baseline.read_text());files=list(root.rglob('*.html'));soups={}
    for path in files:
        rel=path.relative_to(root);route='/404/' if str(rel)=='404.html' else '/' if str(rel)=='index.html' else '/'+str(rel.parent)+'/'
        soups[route]=BeautifulSoup(path.read_text(),'html.parser')
    if len(soups)!=24:errors.append(f'Expected 22 canonical pages, consulting compatibility and a 404 page, got {len(soups)}')
    for route,s in soups.items():
        if len(s.select('h1'))!=1:errors.append(route+': expected one H1')
        ids=[e['id'] for e in s.select('[id]')]
        if len(ids)!=len(set(ids)):errors.append(route+': duplicate IDs')
        for tag in s.select('script[type="application/ld+json"]'):
            try:json.loads(tag.string)
            except (ValueError,TypeError):errors.append(route+': malformed schema')
        for el in s.select('[href],[src]'):
            link=el.get('href',el.get('src',''));u=urlsplit(link)
            if u.scheme or u.netloc or not link:continue
            if u.path.startswith('/'):
                path=root/unquote(u.path.lstrip('/'))
                if path.is_dir():path=path/'index.html'
            elif not u.path:path=root/'404.html' if route=='/404/' else root/route.lstrip('/')/'index.html'
            else:
                errors.append(route+': use root-relative URL '+link);continue
            if not path.is_file():errors.append(route+': missing '+link);continue
            if u.fragment and path.suffix=='.html':
                target_route='/404/' if path.relative_to(root)==Path('404.html') else '/' if path.relative_to(root)==Path('index.html') else '/'+str(path.relative_to(root).parent)+'/'
                dest=soups.get(target_route)
                if dest and not dest.find(id=unquote(u.fragment)):errors.append(route+': missing fragment '+link)
        for el in s.select('[srcset]'):
            for candidate in el['srcset'].split(','):
                src=candidate.strip().split()[0]
                if not src.startswith('/') or not (root/src.lstrip('/')).is_file():errors.append(route+': missing responsive image '+src)
        for image in s.select('img'):
            if not image.get('alt') or not image.get('width') or not image.get('height'):errors.append(route+': incomplete image attributes')
        if len(s.select('img[fetchpriority="high"]'))>1:errors.append(route+': too many priority images')
        scripts=''.join(e.get('src','') for e in s.select('script[src]'))
        if route=='/' and 'terminal' in scripts:errors.append('Terminal loads on Home')
        for k in ['name','property']:
            seen=[e[k] for e in s.select(f'meta[{k}]')]
            if len(seen)!=len(set(seen)):errors.append(route+': duplicate '+k+' metadata')
    for item in baseline_data['assets']:
        if item['file']=='KORVUZ Dark Portfolio Dashboard Montage.png':continue
        p=root/item['file']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:errors.append('Original asset changed or missing: '+item['file'])
    for p in root.rglob('*'):
        if p.is_file() and ('.bak' in p.name or p.suffix=='.md' or any(part in ['tools','content','tests','docs','.tools','node_modules'] for part in p.relative_to(root).parts)):errors.append('Source-only file in release: '+str(p.relative_to(root)))
    for css in (root/'assets/css').glob('*.css'):
        for url in re.findall(r'url\([\"\']?([^\)\"\']+)',css.read_text()):
            if url.startswith('/') and not (root/url.lstrip('/')).is_file():errors.append('Missing CSS asset '+url)
    for folder,budget in [('js',35*1024),('css',40*1024)]:
        size=sum(len(gzip.compress(p.read_bytes())) for p in (root/'assets'/folder).glob('*') if p.is_file())
        # Total JS, including route-only code, is intentionally stricter than the initial route budget.
        if size>budget:errors.append(f'{folder} exceeds compressed byte budget: {size}')
    return errors

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path('dist'));parser.add_argument('--baseline',type=Path,default=Path('docs/redesign/legacy-inventory.json'));a=parser.parse_args();errors=check_artifact(a.root,a.baseline)
    if errors:print('\n'.join(errors));raise SystemExit(1)
    print('PASS: routes, local links/fragments/assets, schema, image dimensions, release exclusions and compressed budgets.')
