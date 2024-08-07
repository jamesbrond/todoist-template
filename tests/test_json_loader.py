"""Test JSON template loader"""
import logging
import unittest
from lib.template.loader.jsonloader import JsonTemplateLoader


class TestJsonLoader(unittest.TestCase):
    """Test JSON template loader"""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        loader = JsonTemplateLoader()
        with open('tests/test.json', 'r', encoding='utf-8') as file:
            self.content = loader.load(file.read())

    def test_json_load(self):
        """Test JSON template loader"""
        self.assertTrue(self.content)

    def test_json_project_inbox(self):
        """Test JSON template Inbox"""
        self.assertIn('Inbox', self.content)
        inbox = self.content['Inbox']
        self.assertEqual(len(inbox['tasks']), 1)

    def test_json_task(self):
        """Test JSON template Inbox task"""
        tasks = self.content['Inbox']['tasks']
        self.assertEqual(tasks[0]['content'], 'delete me')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
