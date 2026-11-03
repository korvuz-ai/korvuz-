"""Canonical resume parsing and personal-page metadata. No duplicated job records."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,re
from bs4 import BeautifulSoup

CAREER_ROUTES=[('/', 'career_home','Home'),('/about/','career_about','About'),('/resume/','career_resume','Resume'),('/experience/','career_experience','Experience'),('/skills/','career_skills','Skills'),('/contact/','career_contact','Contact'),('/404/','career_404','')]

def load_career(root:Path)->dict:
    source=root/'resume/Senior_DevOps_Specialist.html'
    raw=source.read_bytes();soup=BeautifulSoup(raw,'html.parser')
    def text(node):
        if node is None:raise ValueError('Missing canonical resume field')
        return re.sub(r'\s+([,.;:!?)])',r'\1',re.sub(r'\(\s+','(',' '.join(node.get_text(' ',strip=True).split())))
    email=soup.select_one('.contact-row a[href^="mailto:"]')['href'].removeprefix('mailto:')
    if not re.fullmatch(r'[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}',email):raise ValueError('Invalid canonical email')
    links={text(a):a['href'] for a in soup.select('.contact-row a[href^="https://"]')}
    for label,host in [('LinkedIn','linkedin.com'),('GitHub','github.com')]:
        if urlsplit(links[label]).hostname!=host:raise ValueError('Invalid canonical profile URL')
    contacts=[text(item.select('span')[-1]) for item in soup.select('.contact-item') if not item.select('a')]
    jobs=[]
    for node in soup.select('.job'):
        company=text(node.select_one('.job-company')).removeprefix('— ')
        title=text(node.select_one('.job-title')).removesuffix(' — '+company)
        jobs.append({'title':title,'company':company,'date':text(node.select_one('.job-date')),'bullets':[text(li) for li in node.select('li')]})
    skills=[{'category':text(row.select_one('.skill-category')),'items':[text(tag) for tag in row.select('.skill-tag')]} for row in soup.select('.skill-row')]
    education=[{'title':text(row.select_one('.edu-title'))+' '+text(row.select_one('.edu-subtitle')),'date':text(row.select_one('.edu-date'))} for row in soup.select('.edu-row')]
    products=[{'title':text(row.select_one('.product-name')),'description':text(row.select_one('.product-desc'))} for row in soup.select('.product-card')]
    if len(jobs)!=6 or not all(job['bullets'] for job in jobs) or len(skills)!=7 or len(education)!=2:raise ValueError('Incomplete canonical resume')
    summary=text(soup.select_one('.summary'))
    return {'years':text(soup.select_one('.highlight-number')),'name':text(soup.select_one('.header h1')),'title':jobs[0]['title'],'email':email,'phone':contacts[0],'phone_url':'tel:'+re.sub(r'[^+0-9]','',contacts[0]),'location':contacts[1],'linkedin':links['LinkedIn'],'github':links['GitHub'],'summary':summary,'professional_summary':summary.split('Outside work,')[0].strip(),'jobs':jobs,'skills':skills,'education':education,'products':products,'source_sha256':hashlib.sha256(raw).hexdigest()}

def career_seo(career:dict)->dict:
    person={'@type':'Person','@id':'https://korvuz.site/#person','name':career['name'],'jobTitle':career['title'],'url':'https://korvuz.site/','email':'mailto:'+career['email'],'sameAs':[career['linkedin'],career['github']],'worksFor':{'@type':'Organization','name':career['jobs'][0]['company']}}
    descriptions={
      '/':career['name']+' — '+career['title']+' in '+career['location']+'. Explore professional experience across cloud, Linux, networking, automation and platform engineering.',
      '/about/':'Meet '+career['name']+'. A career spanning systems and networking, cloud architecture, automation and DevOps delivery.',
      '/resume/':'Professional resume for '+career['name']+'. Explore verified experience, technical skills and education, or download the original resume PDF.',
      '/experience/':'Career timeline for '+career['name']+', with roles, employers, dates and responsibilities from the Senior DevOps Specialist resume.',
      '/skills/':'Technical skills across cloud, containers, CI/CD, infrastructure as code, observability, security, networking and systems.',
      '/contact/':'Contact '+career['name']+' for DevOps and cloud opportunities, technical collaboration and professional connections.',
      '/404/':'This page could not be found. Return to the career site or view the professional resume.'}
    result={}
    for route,_,label in CAREER_ROUTES:
        canonical='https://korvuz.site'+('/404.html' if route=='/404/' else route)
        title=(career['name']+' — '+career['title'] if route=='/' else ('Page not found' if route=='/404/' else label+' — '+career['name']))+' | KORVUZ'
        metas=[{'name':'description','content':descriptions[route]},{'name':'author','content':career['name']},{'name':'robots','content':'noindex, follow' if route=='/404/' else 'index, follow'},{'property':'og:title','content':title},{'property':'og:description','content':descriptions[route]},{'property':'og:url','content':canonical},{'property':'og:type','content':'website'},{'property':'og:site_name','content':'KORVUZ'},{'property':'og:locale','content':'en_US'},{'property':'og:image','content':'https://korvuz.site/og-image.png'},{'name':'twitter:card','content':'summary_large_image'},{'name':'twitter:title','content':title},{'name':'twitter:description','content':descriptions[route]}]
        schema={'@context':'https://schema.org','@type':'ContactPage' if route=='/contact/' else 'WebPage' if route=='/404/' else 'ProfilePage','name':title,'url':canonical}
        if route!='/404/':schema['mainEntity']=person
        result[route]={'title':title,'canonical':canonical,'meta':metas,'structured_data':[schema]}
    return result
