"""One-time migration from the preserved legacy HTML; never run as part of a build."""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
IDS=['invoiceai','linecrm','fiatline','english-reader','devops-kb']
URLS=['invoice','crm','line','en','doc']
TITLES=['InvoiceAI','LineCRM','FiatLine','English Reader','DevOps KB']

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def rewrite_link(href):
    exact={'/#calc':'/pricing/#calculator','#calc':'/pricing/#calculator','/#services':'/services/','#services':'/services/','/#contact':'/contact/','#contact':'/contact/','/#sandbox':'/lab/#terminal','#sandbox':'/lab/#terminal','/#stack':'/about/#stack','#stack':'/about/#stack'}
    if href in exact:return exact[href]
    if href.startswith('/consult/'):
        return '/services/'+('#'+href.split('#',1)[1] if '#' in href else '#consulting')
    return href

def clean(fragment,demote=False):
    s=BeautifulSoup(str(fragment),'html.parser')
    for e in s.select('script,style,i'): e.decompose()
    for e in s.find_all(True):
        old=e.get('class',[]); classes=[]
        if 'grid' in old: classes.append('legacy-grid')
        if 'bg-paper' in old and 'border' in old: classes.append('panel')
        if e.name=='a' and any(x in old for x in ['bg-ink','bg-sage']): classes.append('button')
        if 'no-print' in old: classes.append('no-print')
        for attr in list(e.attrs):
            if attr not in ['href','src','alt','width','height','id','target','rel','colspan','rowspan','scope','datetime','open','aria-label']:del e[attr]
        if classes:e['class']=classes
        if e.has_attr('href'):e['href']=rewrite_link(e['href'])
        if demote and e.name=='h1':e.name='h2'
    for table in list(s.select('table')):
        wrap=s.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':'ตารางข้อมูล'});table.wrap(wrap)
    return str(s)

def main():
    home=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
    work=BeautifulSoup((ROOT/'work/index.html').read_text(),'html.parser').select_one('main .prose-k')
    headings=work.find_all('h2',recursive=False)
    projects=[]
    tags=[['Next.js 14','TypeScript','Gemini API','Docker','AWS'],['LINE API','PostgreSQL','Redis','Docker Compose'],['LINE API','OCR','PostgreSQL'],['Education','Web','Thai definitions'],['Vanilla JS','Zero dependencies','DevOps']]
    categories=['AI / Web application','LINE / CRM / Automation','LINE / OCR / Finance','Education / Web','DevOps / Knowledge']
    for i,pid in enumerate(IDS):
        paras=[]
        for sib in headings[i].next_siblings:
            if getattr(sib,'name',None)=='h2':break
            if getattr(sib,'name',None)=='p':paras.append(sib.get_text(' ',strip=True))
        projects.append({'id':pid,'title':TITLES[i],'live_url':f'https://{URLS[i]}.korvuz.site/','category':categories[i], 'summary':paras[0].split(' — ',1)[-1], 'problem':paras[1], 'solution':paras[0].split(' — ',1)[-1], 'engineering':paras[1], 'stack':tags[i], 'stack_detail':paras[2] if len(paras)>2 else '', 'featured':i<3, 'source_heading':headings[i].get_text(' ',strip=True)})
    for project in projects:
        project['legacy_home_details']=''
        for card in home.select('#work .work-card'):
            url=card.find('a',href=project['live_url'].rstrip('/'))
            if url and card.find('p'):project['legacy_home_details']=card.find('p').get_text(' ',strip=True)
    write_json(ROOT/'content/projects.json',projects)
    write_json(ROOT/'content/project-media.json',{'version':1,'projects':{pid:{'cover':None,'screenshots':[]} for pid in IDS}})
    write_json(ROOT/'content/site.json',{'name':'Korvuz','email':'korvuznox@gmail.com','github':'https://github.com/korvuz-ai','resume':'/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf','nav':[{'label':l,'url':u} for l,u in [('Work','/work/'),('Services','/services/'),('Pricing','/pricing/'),('About','/about/'),('Blog','/blog/'),('Resume','/resume/')]]})
    calc=home.select_one('#calc');bases=[];opts=[]
    for i,inp in enumerate(calc.select('input[name="base"]')):
        bases.append({'id':['static','wordpress','cloud'][i],'name':['Static website','WordPress','Cloud / DevOps'][i],'price':int(inp['value']),'group':inp['data-group']})
    for group in calc.select('.calc-group'):
        for i,label in enumerate(group.select('label')):
            inp=label.find('input');spans=label.find_all('span',recursive=False)
            opts.append({'id':group['data-group']+'-'+str(i),'group':group['data-group'],'name':spans[0].get_text(' ',strip=True),'price':int(inp['value']),'kind':inp['data-kind']})
    write_json(ROOT/'content/pricing.json',{'bases':bases,'options':opts,'inquiry':'mailto:korvuznox@gmail.com?subject=สอบถามทำเว็บ/วางระบบ Cloud'})
    # Retain complete narrative sections and consulting/resume text in authored fragments.
    for key,selector in [('experience','#experience'),('stack','#stack'),('approach','#approach')]:
        el=home.select_one(selector); (ROOT/f'content/pages/{key}.html').write_text(clean(el))
    packages=home.select_one('#services > div.grid')
    if packages is None:packages=home.select_one('#services .grid')
    (ROOT/'content/pages/packages.html').write_text(clean(packages))
    for key,name in [('resume','resume/index.html'),('consulting','consult/index.html')]:
        main_el=BeautifulSoup((ROOT/name).read_text(),'html.parser').main
        breadcrumb=main_el.find('nav',recursive=False)
        if breadcrumb:breadcrumb.decompose()
        (ROOT/f'content/pages/{key}.html').write_text(clean(main_el.decode_contents(),demote=True))
        if key=='resume':
            education=next(x for x in main_el.select('section') if 'Education & internship' in x.get_text())
            (ROOT/'content/pages/education.html').write_text(clean(education))
    shared=[]
    for sib in headings[5].next_siblings:
        if getattr(sib,'name',None)=='p':shared.append(clean(sib))
        elif getattr(sib,'name',None)=='div':break
    (ROOT/'content/pages/deployment.html').write_text('\n'.join(shared))
    # Index descriptors/dates come from actual published cards; articles retain all main content.
    index=BeautifulSoup((ROOT/'blog/index.html').read_text(),'html.parser')
    articles=[]
    for file in sorted((ROOT/'blog').glob('*/index.html')):
        s=BeautifulSoup(file.read_text(),'html.parser');slug=file.parent.name
        article=s.select_one('article'); main_el=s.main;breadcrumb=main_el.find('nav',recursive=False)
        if breadcrumb:breadcrumb.decompose()
        (ROOT/f'content/blog/{slug}.html').write_text(clean(main_el.decode_contents()))
        link=index.select_one(f'a[href="/blog/{slug}/"]')
        articles.append({'slug':slug,'title':article.h1.get_text(' ',strip=True),'summary':link.get_text(' ',strip=True) if link else article.p.get_text(' ',strip=True)})
    write_json(ROOT/'content/articles.json',articles)
    baseline=json.loads((ROOT/'docs/redesign/legacy-inventory.json').read_text());seo={}
    for item in baseline['pages']:
        seo[item['route']]={'title':item['title'],'meta':item['meta'],'canonical':'https://korvuz.site'+item['route'],'structured_data':item['structured_data']}
    newpages={'/services/':('Services — รับทำเว็บ, AI Automation และ Cloud | Korvuz','บริการพัฒนาเว็บไซต์ LINE และ AI Automation วางระบบ AWS DevOps และที่ปรึกษา พร้อมขอบเขตงานชัดเจน'),'/pricing/':('Pricing — ราคาทำเว็บและ Cloud DevOps | Korvuz','ราคาเว็บไซต์ Static WordPress Cloud DevOps และที่ปรึกษา พร้อมเครื่องมือคำนวณราคาประเมิน'),'/about/':('About — Engineer & Independent Builder | Korvuz','รู้จัก Korvuz ประสบการณ์ Cloud DevOps ระบบเครือข่าย และแนวคิดเบื้องหลังโปรดักต์ที่สร้างเอง'),'/contact/':('Contact — เริ่มคุยเรื่องโปรเจกต์ | Korvuz','ติดต่อ Korvuz เพื่อคุยเรื่องเว็บไซต์ AI LINE Automation และระบบ Cloud DevOps ผ่านอีเมล'),'/lab/':('Lab — Interactive Terminal | Korvuz','ทดลองใช้ terminal จำลองเพื่อรู้จัก Korvuz โปรเจกต์ ประสบการณ์ และช่องทางติดต่อ')}
    for p in projects:newpages['/work/'+p['id']+'/']=(p['title']+' — Case Study | Korvuz',p['summary'])
    for route,(title,desc) in newpages.items():
        seo[route]={'title':title,'canonical':'https://korvuz.site'+route,'meta':[{'name':'description','content':desc},{'name':'robots','content':'index, follow, max-image-preview:large'},{'property':'og:type','content':'website'},{'property':'og:title','content':title},{'property':'og:description','content':desc},{'property':'og:url','content':'https://korvuz.site'+route},{'property':'og:image','content':'https://korvuz.site/og-image.png'},{'name':'twitter:card','content':'summary_large_image'},{'name':'twitter:title','content':title},{'name':'twitter:description','content':desc},{'name':'twitter:image','content':'https://korvuz.site/og-image.png'}],'structured_data':[]}
    # URL-bearing schema changes reflect intentionally relocated content, preserving facts.
    def relocate(value):
        if isinstance(value,str):return value.replace('https://korvuz.site/consult/','https://korvuz.site/services/').replace('https://korvuz.site/#services','https://korvuz.site/services/')
        if isinstance(value,list):return [relocate(v) for v in value]
        if isinstance(value,dict):return {k:relocate(v) for k,v in value.items()}
        return value
    seo['/']['structured_data']=relocate(seo['/']['structured_data'])
    seo['/services/']['structured_data']=relocate(seo['/consult/']['structured_data'])
    seo['/services/']['structured_data']=json.loads(json.dumps(seo['/services/']['structured_data']).replace('https://korvuz.site/services/#page','https://korvuz.site/services/#page'))
    seo['/consult/']={'title':'Consulting has moved — Korvuz','canonical':'https://korvuz.site/services/','meta':[{'name':'robots','content':'noindex, follow'}],'structured_data':[]}
    write_json(ROOT/'content/seo.json',seo)
    (ROOT/'docs/redesign/content-map.md').write_text('''# Content migration map\n\n- Home experience → Home summary + About original full section + Resume unchanged chronology.\n- Home stack/approach → About complete original sections.\n- Home project narratives → Work and individual case studies; original technical details preserved.\n- Home packages → Pricing full inclusions, Services summary.\n- Home calculator → Pricing exact values and group behavior.\n- Consulting entire main body → Services, rates also on Pricing.\n- Resume entire main body → Resume, with new shared chrome.\n- Six blog main bodies → same six routes; moved links updated.\n- Work shared deployment and metrics limitation → Work and case studies.\n- Intro modal intentionally removed; navigation replaced; terminal moved to Lab.\n- Factual contact URLs preserved; playful terminal history labeled simulation.\n\nLegacy Tailwind classes and decorative icons removed during migration. Text is not summarized away in the retained authored fragments.\n''')

if __name__=='__main__':main()
