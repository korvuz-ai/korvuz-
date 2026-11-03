import unittest,json,re,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from tools.migrate_content import clean
class MigrationTests(unittest.TestCase):
 def test_all_article_and_resume_narratives_retained(self):
  for p in Path('blog').glob('*/index.html'):
   old=BeautifulSoup(p.read_text(),'html.parser').article;new=BeautifulSoup(Path('dist/blog',p.parent.name,'index.html').read_text(),'html.parser').article
   self.assertEqual(old.get_text(' ',strip=True),new.get_text(' ',strip=True),p.parent.name)
  from tools.career import load_career
  career=load_career(Path('.'))
  new=BeautifulSoup(Path('dist/resume/index.html').read_text(),'html.parser').select_one('.resume-content').get_text(' ',strip=True)
  for job in career['jobs']:
   for value in [job['title'],job['company'],job['date']]+job['bullets']:self.assertIn(value,new)
  for item in career['education']:self.assertIn(item['title'],new)
 def test_all_original_metadata_except_documented_changes(self):
  baseline=json.loads(Path('docs/redesign/legacy-inventory.json').read_text())
  for page in baseline['pages']:
   if page['route']=='/consult/':continue
   soup=BeautifulSoup(Path('dist',page['file']).read_text(),'html.parser')
   primary=page['route'] in ['/','/about/','/resume/','/contact/']
   if primary:self.assertIn('Nuntawat Fangritlong',soup.title.get_text())
   else:self.assertEqual(soup.title.get_text(),page['title'])
   self.assertEqual(soup.select_one('link[rel="canonical"]')['href'],'https://korvuz.site'+page['route'])
   for meta in page['meta']:
    if primary:continue
    if 'charset'in meta or meta.get('name') in ['viewport','theme-color']:continue
    self.assertIsNotNone(soup.find('meta',attrs=meta),(page['route'],meta))
 def test_consulting_copy_and_five_narratives(self):
  old=BeautifulSoup(Path('consult/index.html').read_text(),'html.parser').main;old.nav.decompose()
  new=BeautifulSoup(Path('dist/services/index.html').read_text(),'html.parser').select_one('#consulting')
  self.assertEqual(old.get_text(' ',strip=True),new.get_text(' ',strip=True))
  projects=json.loads(Path('content/projects.json').read_text())
  for p in projects:
   new=BeautifulSoup(Path('dist/work',p['id'],'index.html').read_text(),'html.parser').get_text(' ',strip=True)
   for value in [p['summary'],p['problem'],p['stack_detail']]:self.assertIn(value,new)
