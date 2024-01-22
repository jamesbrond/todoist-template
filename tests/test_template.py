"""Test Unit for Template class"""
import unittest
from lib.template import Template


class TestTemplate(unittest.TestCase):
    """Test Unit for Template class"""

    def setUp(self):
        self.variables = {
            "test_name": "name",
            "test_date": "today",
            "test_label": "test"
        }

    def test_load_existing_yml_template1(self):
        """Load existing YAML template with one project"""
        with open('tests/test.yml', 'r', encoding='utf8') as file:
            template = Template(file)
            tpl_obj = template.render(self.variables)
        self.assertIsInstance(tpl_obj, dict)
        self.assertEqual(len(tpl_obj), 1)

    def test_load_existing_yml_template2(self):
        """Load existing YAML template with two projects"""
        with open('tests/test2.yml', 'r', encoding='utf8') as file:
            template = Template(file)
            tpl_obj = template.render(self.variables)
        self.assertIsInstance(tpl_obj, list)
        self.assertEqual(len(tpl_obj), 2)

    def test_load_existing_json_template(self):
        """Load existing JSON template"""
        with open('tests/test.json', 'r', encoding='utf8') as file:
            template = Template(file)
            tpl_obj = template.render(self.variables)
        self.assertIsInstance(tpl_obj, dict)
        self.assertEqual(len(tpl_obj), 1)

    def test_load_existing_csv_template(self):
        """Load existing CSV template"""
        with open('tests/test.csv', 'r', encoding='utf8') as file:
            template = Template(file)
            tpl_obj = template.render(self.variables)
        self.assertIsInstance(tpl_obj, list)
        self.assertEqual(len(tpl_obj), 2)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
