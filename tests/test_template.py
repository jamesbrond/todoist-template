"""Test Unit for Template class"""
import unittest
from lib.template import Template


class TestTemplate(unittest.TestCase):
    """Test Unit for Template class"""

    def setUp(self):
        self.template = Template()
        self.placeholders = {
            "test_name": "name",
            "test_date": "today",
            "test_label": "test"
        }

    def test_load_existing_yml_template1(self):
        """Load existing YAML template with one project"""
        with open('tests/test.yml', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        self.assertIsInstance(tpl_obj, dict)
        self.assertEqual(len(tpl_obj), 1)

    def test_load_existing_yml_template2(self):
        """Load existing YAML template with two projects"""
        with open('tests/test2.yml', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        self.assertIsInstance(tpl_obj, list)
        self.assertEqual(len(tpl_obj), 2)

    def test_load_existing_json_template(self):
        """Load existing JSON template"""
        with open('tests/test.json', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        self.assertIsInstance(tpl_obj, dict)
        self.assertEqual(len(tpl_obj), 1)

    def test_load_existing_csv_template(self):
        """Load existing CSV template"""
        with open('tests/test.csv', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        self.assertIsInstance(tpl_obj, list)
        self.assertEqual(len(tpl_obj), 2)

    def test_parse_no_placeholders(self):
        """No placeholders"""
        with open('tests/test2.yml', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        parsed_tpl_obj = self.template.parse_template(tpl_obj)
        self.assertEqual(tpl_obj, parsed_tpl_obj)

    def test_parse_simple_placeholders(self):
        """Simple placeholders replacement"""
        with open('tests/test2.yml', 'r', encoding='utf8') as file:
            tpl_obj = self.template.load_template(file)
        parsed_tpl_obj = self.template.parse_template(tpl_obj, self.placeholders)
        self.assertNotEqual(tpl_obj, parsed_tpl_obj)

    def test_simple_replacement_not_string(self):
        """Simple replacement not string"""
        orig = 44
        self.assertEqual(self.template._replace(orig, self.placeholders), 44)

    def test_simple_replacement(self):
        """Simple replacement"""
        orig = "Test {test_name}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test name")

    def test_simple_replacement_with_fallback1(self):
        """Replacement with fallback 1"""
        orig = "Test {test_name|nobody}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test name")

    def test_simple_replacement_with_fallback2(self):
        """Replacement with fallback 2"""
        orig = "Test {test_foo|not foo}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test not foo")

    def test_array(self):
        """Replacement in array"""
        orig = ["{test_name}", "{test_foo|not foo}"]
        self.assertEqual(self.template._replace(orig, self.placeholders), ["name", "not foo"])

    def test_dict(self):
        """Replacement in dictionary"""
        orig = {
            "id": 3,
            "name": "{test_name}",
            "descr": "{test_foo|not foo}"
        }
        self.assertEqual(self.template._replace(orig, self.placeholders),
                         {"id": 3, "name": "name", "descr": "not foo"})


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
