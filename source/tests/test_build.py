import unittest,tempfile,json,shutil
from pathlib import Path
from tools.build import build_site
class BuildTests(unittest.TestCase):
 def test_output_cannot_overwrite_source(self):
  for path in [Path('.'),Path('content'),Path('assets'),Path('templates'),Path('blog'),Path('work')]:
   with self.assertRaises(ValueError):build_site(Path('.'),path)
 def test_bad_content_leaves_existing_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);shutil.copytree('content',root/'content');out=root/'dist';out.mkdir();(out/'sentinel').write_text('previous valid build')
   p=root/'content/projects.json';data=json.loads(p.read_text());data[0]['id']='unknown';p.write_text(json.dumps(data))
   with self.assertRaises(ValueError):build_site(root,out)
   self.assertEqual((out/'sentinel').read_text(),'previous valid build')
 def test_unowned_external_output_is_not_replaced(self):
  with tempfile.TemporaryDirectory() as d:
   output=Path(d)/'unrelated';output.mkdir();(output/'keep.txt').write_text('unrelated owner file')
   with self.assertRaises(ValueError):build_site(Path('.'),output)
   self.assertEqual((output/'keep.txt').read_text(),'unrelated owner file')
