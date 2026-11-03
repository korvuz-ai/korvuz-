import copy,json,unittest
from pathlib import Path
from bs4 import BeautifulSoup
from tools.content import load_content


class HubTests(unittest.TestCase):
 def test_records_support_optional_lifecycle_without_inventing_status(self):
  from tools.content import project_records
  data=load_content(Path('.'))
  original=copy.deepcopy(data.projects)
  records=project_records(data)
  self.assertEqual(data.projects,original)
  self.assertEqual([p['id'] for p in records],[p['id'] for p in original])
  for p in records:
   self.assertIsNone(p['status'])
   self.assertEqual(p['case_study_url'],f"/work/{p['id']}/")
   self.assertEqual(p['media'],data.media['projects'][p['id']])
  data.projects[0]['status']='building'
  self.assertEqual(project_records(data)[0]['status'],'building')
  data.projects[0]['status']='made-up'
  with self.assertRaises(ValueError):project_records(data)

 def test_project_actions_are_independent_and_unavailable_products_are_disabled(self):
  soup=BeautifulSoup(Path('dist/work/index.html').read_text(),'html.parser')
  unavailable=set(json.loads(Path('content/project-availability.json').read_text())['unavailable'])
  for project in json.loads(Path('content/projects.json').read_text()):
   card=soup.select_one(f"[data-project='{project['id']}']")
   self.assertEqual(card.select_one('.case-link')['href'],f"/work/{project['id']}/")
   if project['id'] in unavailable:
    self.assertIsNone(card.select_one('.product-link[href]'))
    self.assertIsNotNone(card.select_one('.product-link[aria-disabled="true"]'))
   else:self.assertEqual(card.select_one('.product-link')['href'],project['live_url'])

