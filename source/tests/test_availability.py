import json, unittest
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

UNAVAILABLE={'invoice.korvuz.site':'invoiceai','crm.korvuz.site':'linecrm','line.korvuz.site':'fiatline','en.korvuz.site':'english-reader'}

class AvailabilityTests(unittest.TestCase):
 def test_unavailable_projects_never_expose_external_navigation(self):
  for path in Path('dist').rglob('*.html'):
   soup=BeautifulSoup(path.read_text(),'html.parser')
   for link in soup.select('a[href]'):
    self.assertNotIn(urlsplit(link['href']).hostname,UNAVAILABLE,str(path)+' '+link['href'])
   for schema in soup.select('script[type="application/ld+json"]'):
    for domain in UNAVAILABLE:self.assertNotIn(domain,schema.get_text(),str(path))
  for domain in UNAVAILABLE:self.assertNotIn(domain,Path('dist/sitemap.xml').read_text())

 def test_resume_falls_back_to_internal_case_studies_and_available_project_stays_live(self):
  soup=BeautifulSoup(Path('dist/work/index.html').read_text(),'html.parser')
  for pid in UNAVAILABLE.values():self.assertTrue(soup.select(f'a[href="/work/{pid}/"]'),pid)
  work=BeautifulSoup(Path('dist/work/index.html').read_text(),'html.parser')
  self.assertTrue(work.select('[data-project="devops-kb"] a[href="https://doc.korvuz.site/"]'))
  self.assertIsNotNone(json.loads(Path('content/projects.json').read_text())[0]['live_url'])
