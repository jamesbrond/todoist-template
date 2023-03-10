import logging
import unittest
from lib.loader.yamlloader import YamlTemplateLoader


class TestYamlLoader(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        loader = YamlTemplateLoader()
        with open('tests/test.yml', 'r', encoding='utf-8') as file:
            self.content = loader.load(file)

    def test_yaml_load(self):
        self.assertTrue(self.content)
        self.assertEqual(len(self.content), 1)

    def test_yaml_project_inbox(self):
        self.assertIn('Inbox', self.content)
        inbox = self.content['Inbox']
        self.assertEqual(len(inbox['tasks']), 1)

    def test_yaml_task(self):
        tasks = self.content['Inbox']['tasks']
        self.assertEqual(tasks[0]['content'], 'delete {test_name|me}')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]