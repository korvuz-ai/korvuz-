"""Build only into a separate, validated static artifact. Never changes the live host."""
from pathlib import Path
import sys
if __package__ in (None,''):sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse,copy,hashlib,json,os,shutil,tempfile
from dataclasses import dataclass
from xml.etree import ElementTree as ET
from urllib.parse import urlsplit
from jinja2 import Environment,FileSystemLoader,select_autoescape,StrictUndefined
from tools.content import load_content,project_records
from tools.media import validate_media,process_image,source_path
from tools.fonts import build_fonts
from tools.availability import unavailable_destinations,rewrite_links,rewrite_schema
from tools.career import load_career,career_seo,CAREER_ROUTES

@dataclass
class BuildReport:
    routes:list
    files:int
    bytes:int

SERVICES=[
 {'name':'Web & Product','icon':'web','description':'เว็บไซต์ที่เหมาะกับธุรกิจ ตั้งแต่ Landing Page ถึงระบบหลังบ้าน','items':['Landing pages & company websites','WordPress / WooCommerce','Web applications & internal tools'],'price':'From ฿8,000','url':'/pricing/#calculator'},
 {'name':'AI & Automation','icon':'ai','description':'เชื่อม AI และ LINE เข้ากับงานที่ทำอยู่ ลดขั้นตอนซ้ำ ๆ','items':['AI integrations','LINE workflows & chatbots','OCR & business automation'],'price':'Scoped after discussion','url':'/contact/'},
 {'name':'Cloud & DevOps','icon':'cloud','description':'ระบบเบื้องหลังที่ deploy ได้ ดูแลต่อได้ และเข้าใจได้','items':['AWS migration & infrastructure','Docker / CI/CD / Terraform','Monitoring & automation'],'price':'From ฿15,000','url':'/pricing/#calculator'},
 {'name':'Consulting','icon':'consult','description':'ช่วยตรวจระบบ วางแผน และตัดสินใจทางเทคนิคก่อนลงทุน','items':['Architecture & system review','Cloud cost optimization','Migration planning & retainer'],'price':'From ฿1,500 / hr','url':'/services/#consulting'}]

def build_site(root:Path,output:Path)->BuildReport:
    root=root.resolve();output=output.resolve()
    if root==output or root.is_relative_to(output) or (output.is_relative_to(root) and output != root/'dist'):raise ValueError('Output must be a separate build directory')
    if output.exists():
        if not output.is_dir():raise ValueError('Output must be a directory')
        if any(output.iterdir()):
            manifest_file=output/'release-manifest.json'
            if not manifest_file.is_file():raise ValueError('Refusing to replace an unrelated output directory')
            try:
                previous=json.loads(manifest_file.read_text())
                existing={str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and p!=manifest_file}
                if not isinstance(previous,dict) or set(previous)!=existing:raise ValueError('Output contains untracked files')
                if any(hashlib.sha256((output/name).read_bytes()).hexdigest()!=digest for name,digest in previous.items()):raise ValueError('Output was edited manually; preserve those changes before rebuilding')
            except (OSError,TypeError,json.JSONDecodeError) as error:raise ValueError('Cannot validate previous release manifest') from error
    data=copy.deepcopy(load_content(root));validate_media(data.media,root)
    career=load_career(root);data.seo.update(career_seo(career))
    data.site.update(email=career['email'],linkedin=career['linkedin'],local='https://local.korvuz.site/')
    unavailable=unavailable_destinations(data.projects,data.unavailable)
    data.pages={name:rewrite_links(html,unavailable) for name,html in data.pages.items()}
    for article in data.articles:article['body_html']=rewrite_links(article['body_html'],unavailable)
    data.seo=rewrite_schema(data.seo,unavailable)
    build_fonts(root,root/'assets/fonts')
    env=Environment(loader=FileSystemLoader(root/'templates'),autoescape=select_autoescape(['html']),undefined=StrictUndefined,trim_blocks=True,lstrip_blocks=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix='.korvuz-build-',dir=output.parent));backup=None
    try:
        for folder in ['css','js','fonts','icons']:shutil.copytree(root/'assets'/folder,staging/'assets'/folder)
        (staging/'assets/js/pricing-data.js').write_text('export default '+json.dumps(data.pricing,ensure_ascii=False,separators=(',',':'))+';\n')
        projects=project_records(data)
        links={p['id']:('/work/'+p['id']+'/' if p['id'] in data.unavailable else p['live_url']) for p in projects}
        (staging/'assets/js/project-links.js').write_text('export default '+json.dumps(links,separators=(',',':'))+';\n')
        for p in projects:
            for item in ([p['media']['cover']] if p['media']['cover'] else [])+p['media']['screenshots']:
                processed=process_image(source_path(root,p['id'],item['src']),staging/'assets/media');item.update(processed)
        registry=CAREER_ROUTES+[('/work/','work','Work'),('/services/','services','Services'),('/pricing/','pricing','Pricing'),('/blog/','blog','Blog'),('/lab/','lab',''),('/consult/','legacy_consult','Services')]
        registry += [('/work/'+p['id']+'/','case_study','Work') for p in projects]
        registry += [('/blog/'+a['slug']+'/','article','Blog') for a in data.articles]
        for route,template,active in registry:
            if route not in data.seo:raise ValueError('Missing route SEO: '+route)
            scripts=[]
            if route in ['/','/consult/']:scripts.append('legacy.js')
            if route=='/pricing/':scripts.append('calculator.js')
            if route=='/contact/':scripts.append('career-contact.js')
            if route=='/lab/':scripts.append('terminal.js')
            primary=template.startswith('career_')
            context={'page':{'route':route,'seo':data.seo[route],'active_nav':active,'scripts':scripts,'language':'en' if primary else 'th','body_class':('career-page ' if primary else '')+'page-'+template.replace('_','-')},'site':data.site,'projects':projects,'pricing':data.pricing,'pages':data.pages,'articles':data.articles,'services':SERVICES,'career':career,'career_nav':CAREER_ROUTES[:-1]}
            if template=='case_study':
                index=next(i for i,p in enumerate(projects) if route=='/work/'+p['id']+'/');context.update(project=projects[index],next_project=projects[(index+1)%len(projects)])
            if template=='article':context['article']=next(a for a in data.articles if route=='/blog/'+a['slug']+'/')
            rendered=env.get_template('pages/'+template+'.html').render(**context)
            file=staging/'404.html' if route=='/404/' else staging/route.strip('/')/'index.html';file.parent.mkdir(parents=True,exist_ok=True);file.write_text(rendered+'\n')
        for name in ['Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf','resume.pdf','DevOps_Engineer.pdf','invoice.jpg','linecrm.jpg','fiatline.jpg','devops.jpg','og-image.png']:shutil.copy2(root/name,staging/name)
        (staging/'robots.txt').write_text((root/'robots.txt').read_text())
        ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
        previous=ET.parse(root/'sitemap.xml').getroot();entries={el.find('{'+ns+'}loc').text:el for el in previous}
        sitemap=ET.Element('{'+ns+'}urlset')
        canonical=[route for route,_,_ in registry if route not in ['/consult/','/404/']]
        for url in ['https://korvuz.site'+r for r in canonical]+[url for url in entries if not url.startswith('https://korvuz.site') and urlsplit(url).hostname not in unavailable]:
            if url in entries:sitemap.append(entries[url])
            else:
                entry=ET.SubElement(sitemap,'{'+ns+'}url');ET.SubElement(entry,'{'+ns+'}loc').text=url;ET.SubElement(entry,'{'+ns+'}lastmod').text='2026-10-15'
        ET.indent(sitemap,space='  ');ET.ElementTree(sitemap).write(staging/'sitemap.xml',encoding='utf-8',xml_declaration=True)
        from tools.check_artifact import check_artifact
        errors=check_artifact(staging,root/'docs/redesign/legacy-inventory.json')
        if errors:raise ValueError('Artifact validation failed:\n'+'\n'.join(errors))
        manifest={str(p.relative_to(staging)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(staging.rglob('*')) if p.is_file()}
        (staging/'release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        if output.exists():
            backup=output.with_name(output.name+'.previous-build')
            if backup.exists():raise ValueError('Previous build recovery folder already exists: '+str(backup))
            output.rename(backup)
        try:staging.rename(output)
        except Exception:
            if backup:backup.rename(output);backup=None
            raise
        if backup:shutil.rmtree(backup)
        files=[p for p in output.rglob('*') if p.is_file()]
        return BuildReport(canonical,len(files),sum(p.stat().st_size for p in files))
    finally:
        if staging.exists():shutil.rmtree(staging)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('dist'));args=parser.parse_args()
    result=build_site(Path(__file__).resolve().parents[1],args.output);print(f'Built {len(result.routes)} canonical pages + legacy consulting redirect; {result.files} files, {result.bytes:,} bytes → {args.output}')
