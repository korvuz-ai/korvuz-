import unittest,json,tempfile,shutil,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
class PortfolioTests(unittest.TestCase):
 def test_home_sequence_and_projects(self):
  s=BeautifulSoup(Path('dist/index.html').read_text(),'html.parser')
  self.assertEqual([e['data-section'] for e in s.select('main > [data-section]')],[])
  self.assertEqual(s.h1.get_text(strip=True),'Nuntawat Fangritlong')
  for pid in ['invoiceai','linecrm','fiatline','english-reader','devops-kb']:
   self.assertTrue(Path(f'dist/work/{pid}/index.html').is_file())
  self.assertEqual(len(s.select('.project-card')),0)
  self.assertNotIn('terminal.js',str(s))
 def test_every_home_project_uses_central_cover_or_placeholder(self):
  home=BeautifulSoup(Path('dist/index.html').read_text(),'html.parser')
  work=BeautifulSoup(Path('dist/work/index.html').read_text(),'html.parser')
  media=json.loads(Path('content/project-media.json').read_text())['projects']
  for pid,record in media.items():
   card=work.select_one(f'[data-project="{pid}"]')
   self.assertIsNotNone(card,pid+' must retain a media-driven Work card')
   case=BeautifulSoup(Path(f'dist/work/{pid}/index.html').read_text(),'html.parser')
   work_card=work.select_one(f'[data-project="{pid}"]')
   if record['cover']:
    images=[card.select_one('img'),work_card.select_one('img'),case.select_one('.case-cover img')]
    for image in images:
     self.assertEqual(image['alt'],record['cover']['alt'])
     self.assertEqual(image['src'],images[0]['src'])
     self.assertEqual(image['srcset'],images[0]['srcset'])
   else:
    for surface in [card,work_card,case.select_one('.case-cover')]:
     self.assertIsNotNone(surface.select_one('.media-placeholder'))
     self.assertIsNone(surface.select_one('img'))

 def test_replacing_one_central_cover_updates_home_work_and_case_study(self):
  from tools.build import build_site
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory)/'source';root.mkdir()
   for folder in ['content','templates','assets','resume']:shutil.copytree(folder,root/folder)
   (root/'docs/redesign').mkdir(parents=True)
   shutil.copy2('docs/redesign/legacy-inventory.json',root/'docs/redesign/legacy-inventory.json')
   for name in ['Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf','resume.pdf','DevOps_Engineer.pdf','invoice.jpg','linecrm.jpg','fiatline.jpg','devops.jpg','og-image.png','robots.txt','sitemap.xml']:
    shutil.copy2(name,root/name)
   replacement=Path('linecrm.jpg').read_bytes()
   (root/'assets/projects/invoiceai/cover-source.jpg').write_bytes(replacement)
   manifest_path=root/'content/project-media.json';manifest=json.loads(manifest_path.read_text())
   manifest['projects']['invoiceai']['cover']['alt']='QA replacement from the central media record'
   manifest_path.write_text(json.dumps(manifest))
   output=Path(directory)/'release';build_site(root,output)
   prefix='/assets/media/'+hashlib.sha256(replacement).hexdigest()[:16]
   sources=[]
   for name,selector in [('work/index.html','[data-project="invoiceai"] img'),('work/invoiceai/index.html','.case-cover img')]:
    soup=BeautifulSoup((output/name).read_text(),'html.parser');image=soup.select_one(selector)
    self.assertEqual(image['alt'],'QA replacement from the central media record')
    self.assertTrue(image['src'].startswith(prefix));sources.append(image['src'])
   self.assertEqual(len(set(sources)),1)
