import logging
import unittest
from lib.loader.csvloader import CsvTemplateLoader


class TestCSVLoader(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        loader = CsvTemplateLoader()
        with open('tests/test.csv', 'r', encoding='utf-8') as file:
            self.content = loader.load(file)

    def test_csv_load(self):
        self.assertTrue(self.content)
        self.assertEqual(len(self.content), 2)

    def test_csv_project_0_inbox(self):
        self.assertIn('Inbox', self.content[0])
        inbox = self.content[0]['Inbox']
        self.assertEqual(len(inbox['tasks']), 1)

    def test_csv_project_1_test_project(self):
        self.assertIn('Test project', self.content[1])
        prj = self.content[1]['Test project']
        self.assertEqual(len(prj['tasks']), 0)

    def test_csv_section(self):
        self.assertIn('Test section', self.content[1])
        sec = self.content[1]['Test section']
        self.assertEqual(len(sec['tasks']), 2)

    def test_csv_task(self):
        tasks = self.content[1]['Test section']['tasks']
        self.assertEqual(tasks[0]['content'], 'Test task 1')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
