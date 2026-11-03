"""Build-time navigation fallbacks; original project and authored records stay intact."""
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

def unavailable_destinations(projects, unavailable):
    return {urlsplit(p['live_url']).hostname:'/work/'+p['id']+'/' for p in projects if p['id'] in unavailable}

def public_url(url, destinations, absolute=False):
    destination=destinations.get(urlsplit(url).hostname)
    return ('https://korvuz.site' if absolute else '')+destination if destination else url

def rewrite_links(html, destinations):
    soup=BeautifulSoup(html,'html.parser')
    for anchor in soup.select('a[href]'):
        original=anchor['href'];replacement=public_url(original,destinations)
        if replacement!=original:
            anchor['href']=replacement
            anchor.attrs.pop('target',None)
            anchor.attrs.pop('rel',None)
    return str(soup)

def rewrite_schema(value, destinations):
    if isinstance(value,dict):return {key:rewrite_schema(item,destinations) for key,item in value.items()}
    if isinstance(value,list):return [rewrite_schema(item,destinations) for item in value]
    if isinstance(value,str) and value.startswith(('https://','http://')):return public_url(value,destinations,absolute=True)
    return value
