import tempfile,unittest
from pathlib import Path
from bs4 import BeautifulSoup

class CareerTests(unittest.TestCase):
 def test_canonical_resume_facts_and_shared_source(self):
  from tools.career import load_career
  career=load_career(Path('.'))
  self.assertEqual(career['name'],'Nuntawat Fangritlong')
  self.assertEqual(career['email'],'nuntawat.works@gmail.com')
  self.assertEqual(career['linkedin'],'https://linkedin.com/in/nuntawat-zeo')
  self.assertEqual(len(career['jobs']),6)
  self.assertEqual(career['jobs'][0]['company'],'Orbix Custodian')
  self.assertEqual(career['jobs'][0]['date'],'Mar 2026 – Present')
  self.assertEqual(career['jobs'][-1]['date'],'Dec 2020 – Sep 2022')
  self.assertEqual(len(career['skills']),7)
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);(root/'resume').mkdir()
   source=Path('resume/Senior_DevOps_Specialist.html').read_text().replace('Nuntawat Fangritlong','Canonical Test Name')
   (root/'resume/Senior_DevOps_Specialist.html').write_text(source)
   self.assertEqual(load_career(root)['name'],'Canonical Test Name')

 def test_home_is_career_first_and_local_is_only_a_gateway(self):
  soup=BeautifulSoup(Path('dist/index.html').read_text(),'html.parser')
  self.assertEqual(soup.h1.get_text(' ',strip=True),'Nuntawat Fangritlong')
  self.assertFalse(soup.select('.project-card,.price-card,.inquiry-form'))
  self.assertEqual(len(soup.select('main a[href="https://local.korvuz.site/"]')),1)
  self.assertTrue(soup.select('main a[href="/resume/"]'))
  self.assertTrue(soup.select('main a[href="/experience/"]'))

 def test_new_career_routes_and_noindex_error_page(self):
  for route in ['experience','skills']:
   soup=BeautifulSoup(Path('dist',route,'index.html').read_text(),'html.parser')
   self.assertEqual(soup.select_one('link[rel=canonical]')['href'],f'https://korvuz.site/{route}/')
  soup=BeautifulSoup(Path('dist/404.html').read_text(),'html.parser')
  self.assertIn('noindex',soup.select_one('meta[name=robots]')['content'])
  self.assertNotIn('/404',Path('dist/sitemap.xml').read_text())
