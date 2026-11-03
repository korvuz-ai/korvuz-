import unittest
from pathlib import Path
from tools.content import load_content

class ContentTests(unittest.TestCase):
    def test_real_content_contract(self):
        data=load_content(Path('.'))
        self.assertEqual([p['id'] for p in data.projects], ['invoiceai','linecrm','fiatline','english-reader','devops-kb'])
        self.assertEqual([p['live_url'] for p in data.projects], ['https://invoice.korvuz.site/','https://crm.korvuz.site/','https://line.korvuz.site/','https://en.korvuz.site/','https://doc.korvuz.site/'])
        self.assertEqual(len(data.articles),6)
        self.assertIn('Senior DevOps Specialist',data.pages['resume'])
        self.assertIn('2020',data.pages['resume'])
        self.assertIn('24/7',data.pages['consulting'])
        self.assertEqual(len(data.pricing['options']),12)
