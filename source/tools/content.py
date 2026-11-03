"""Validated, build-time source content. No public runtime data fetching."""
from dataclasses import dataclass
from pathlib import Path
import json
from urllib.parse import urlparse
import copy
from bs4 import BeautifulSoup

PROJECT_IDS=['invoiceai','linecrm','fiatline','english-reader','devops-kb']
@dataclass
class SiteContent:
    site:dict
    projects:list
    media:dict
    pricing:dict
    seo:dict
    pages:dict
    articles:list
    unavailable:set
    hub:dict

def project_records(data:SiteContent)->list:
    """Join real author records/media once. Never infer lifecycle from DNS health."""
    records=copy.deepcopy(data.projects)
    for project in records:
        status=project.get('status')
        if status not in [None,'live','building','research','experiment','archived']:
            raise ValueError('Unknown project lifecycle status')
        project['status']=status
        project['type']=project.get('type','product')
        project['case_study_url']='/work/'+project['id']+'/'
        project['available']=project['id'] not in data.unavailable
        project['media']=copy.deepcopy(data.media['projects'][project['id']])
    return records

def load_content(root:Path)->SiteContent:
    def load(name):return json.loads((root/'content'/name).read_text())
    projects=load('projects.json')
    if [p['id'] for p in projects]!=PROJECT_IDS:raise ValueError('Project IDs must be the five unique portfolio IDs in configured order')
    for p in projects:
        u=urlparse(p['live_url'])
        if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Unsafe project URL')
        for field in ['title','summary','problem','solution','engineering','stack']:
            if not p.get(field):raise ValueError('Missing project field '+field)
    seo=load('seo.json')
    for route,v in seo.items():
        if not v.get('title') or not v.get('canonical') or not v.get('meta'):raise ValueError('Missing SEO for '+route)
    pages={p.stem:p.read_text() for p in (root/'content/pages').glob('*.html')}
    for name in ['resume','consulting','experience','stack','approach','packages','deployment']:
        if not pages.get(name):raise ValueError('Missing page fragment '+name)
    articles=load('articles.json')
    if len(articles)!=6 or len({a['slug'] for a in articles})!=6:raise ValueError('Six original articles required')
    for a in articles:
        a['body_html']=(root/'content/blog'/f"{a['slug']}.html").read_text()
        document=BeautifulSoup(a['body_html'],'html.parser')
        a['published']=document.select_one('time[datetime]')['datetime']
        a['category']=document.select_one('article > div > span').get_text(' ',strip=True)
        a['excerpt']=document.select_one('article > p').get_text(' ',strip=True)
    availability=load('project-availability.json')
    unavailable=availability.get('unavailable')
    if availability.get('version')!=1 or not isinstance(unavailable,list) or any(not isinstance(pid,str) or pid not in PROJECT_IDS for pid in unavailable) or len(unavailable)!=len(set(unavailable)):
        raise ValueError('Availability requires version 1 and unique known project IDs')
    return SiteContent(load('site.json'),projects,load('project-media.json'),load('pricing.json'),seo,pages,articles,set(unavailable),load('hub.json'))
