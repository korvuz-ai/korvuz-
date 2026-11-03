import unittest,tempfile,json,hashlib,base64
from pathlib import Path
from tools.media_editor import save_media,manifest_digest,EditorError
from tools.content import PROJECT_IDS

class EditorTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'content').mkdir()
  self.manifest={'version':1,'projects':{p:{'cover':None,'screenshots':[]} for p in PROJECT_IDS}}
  (self.root/'content/project-media.json').write_text(json.dumps(self.manifest))
  self.digest=manifest_digest(self.root)
 def tearDown(self):self.temp.cleanup()
 def payload(self):
  self.manifest['projects']['invoiceai']['cover']={'src':'upload:new','alt':'Actual screenshot','fit':'contain','position':'50% 50%'}
  return {'version':1,'manifest':self.manifest,'uploads':[{'id':'new','projectId':'invoiceai','filename':'capture.jpg','data':base64.b64encode(Path('invoice.jpg').read_bytes()).decode()}]}
 def test_save_and_conflict(self):
  result=save_media(self.root,self.payload(),self.digest)
  self.assertTrue(result['saved']);self.assertNotEqual(result['digest'],self.digest)
  with self.assertRaises(EditorError) as ctx:save_media(self.root,self.payload(),self.digest)
  self.assertEqual(ctx.exception.status,409)
 def test_invalid_input_does_not_replace_manifest(self):
  payload=self.payload();payload['uploads'][0]['data']=base64.b64encode(b'<svg/>').decode()
  with self.assertRaises(ValueError):save_media(self.root,payload,self.digest)
  self.assertEqual(manifest_digest(self.root),self.digest)
 def test_cross_project_or_path_injection_rejected(self):
  payload=self.payload();payload['uploads'][0]['projectId']='../../etc'
  with self.assertRaises(ValueError):save_media(self.root,payload,self.digest)
  self.assertEqual(manifest_digest(self.root),self.digest)
