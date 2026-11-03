import unittest,json,hashlib,tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from tools.check_artifact import check_artifact
from tools.build import build_site
class ReleaseTests(unittest.TestCase):
 def test_artifact_and_original_source_integrity(self):
  self.assertEqual(check_artifact(Path('dist'),Path('docs/redesign/legacy-inventory.json')),[])
  baseline=json.loads(Path('docs/redesign/legacy-inventory.json').read_text())
  for item in baseline['pages']+baseline['assets']:
   if item['file']=='KORVUZ Dark Portfolio Dashboard Montage.png':continue  # archived 2026-10-28
   if item['file']=='resume/index.html':
    # Its original narrative is preserved in the migration inventory; the
    # supplied resume directory now contains Senior_DevOps_Specialist.html.
    self.assertEqual(hashlib.sha256(Path('content/pages/resume.html').read_bytes()).hexdigest(),'410fb78fa3d46a27a42a191b834c6e001422947995d3622acccc89198103c280')
    continue
   self.assertEqual(hashlib.sha256(Path(item['file']).read_bytes()).hexdigest(),item['sha256'],item['file'])
  s=BeautifulSoup(Path('dist/index.html').read_text(),'html.parser')
  self.assertIsNone(s.select_one('#introModal'))
  self.assertTrue(all('cdn' not in e.get('src','') for e in s.select('script[src]')))
 def test_schema_preserves_original_facts(self):
  baseline=json.loads(Path('docs/redesign/legacy-inventory.json').read_text())
  for page in baseline['pages']:
   if page['route']=='/consult/':continue
   if page['route'] in ['/','/about/','/resume/','/contact/']:
    soup=BeautifulSoup(Path('dist',page['file']).read_text(),'html.parser')
    person=json.loads(soup.select_one('script[type="application/ld+json"]').string)['mainEntity']
    self.assertEqual(person['name'],'Nuntawat Fangritlong')
    self.assertEqual(person['jobTitle'],'Senior DevOps Specialist')
    self.assertEqual(person['email'],'mailto:nuntawat.works@gmail.com')
    continue
   expected=page['structured_data']
   if page['route']=='/':expected=json.loads(json.dumps(expected).replace('https://korvuz.site/consult/','https://korvuz.site/services/').replace('https://korvuz.site/#services','https://korvuz.site/services/'))
   unavailable={'https://invoice.korvuz.site/':'https://korvuz.site/work/invoiceai/','https://crm.korvuz.site/':'https://korvuz.site/work/linecrm/','https://line.korvuz.site/':'https://korvuz.site/work/fiatline/','https://en.korvuz.site/':'https://korvuz.site/work/english-reader/'}
   encoded=json.dumps(expected)
   for original,fallback in unavailable.items():encoded=encoded.replace(original,fallback)
   expected=json.loads(encoded)
   soup=BeautifulSoup(Path('dist',page['file']).read_text(),'html.parser')
   self.assertEqual([json.loads(e.string) for e in soup.select('script[type="application/ld+json"]')],expected,page['route'])
 def test_two_builds_have_identical_bytes(self):
  with tempfile.TemporaryDirectory() as d:
   output=Path(d)/'release';build_site(Path('.'),output);first=(output/'release-manifest.json').read_bytes();build_site(Path('.'),output);self.assertEqual((output/'release-manifest.json').read_bytes(),first)
 def test_gallery_caption_is_optional_and_escaped(self):
  from unittest.mock import patch
  from tools.content import load_content
  data=load_content(Path('.'));cover=data.media['projects']['invoiceai']['cover']
  data.media['projects']['invoiceai']['screenshots']=[{'id':'detail','src':cover['src'],'alt':'Invoice detail'}]
  with tempfile.TemporaryDirectory() as d,patch('tools.build.load_content',return_value=data):
   output=Path(d)/'release';build_site(Path('.'),output)
   soup=BeautifulSoup((output/'work/invoiceai/index.html').read_text(),'html.parser')
   self.assertEqual(len(soup.select('.screenshot-gallery img')),1)
   self.assertEqual(len(soup.select('.screenshot-gallery figcaption')),0)
  data.media['projects']['invoiceai']['screenshots'][0]['caption']='<img src=x onerror=alert(1)>'
  with tempfile.TemporaryDirectory() as d,patch('tools.build.load_content',return_value=data):
   output=Path(d)/'release';build_site(Path('.'),output)
   soup=BeautifulSoup((output/'work/invoiceai/index.html').read_text(),'html.parser')
   self.assertEqual(soup.select_one('figcaption').get_text(),'<img src=x onerror=alert(1)>')
   self.assertEqual(len(soup.select('figcaption img')),0)
