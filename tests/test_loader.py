"""Test factory template loader"""
import logging
import unittest
from template.loader.plaintextloader import PlainTextTemplateLoader
from template.loader.jsonloader import JsonTemplateLoader
from template.loader.yamlloader import YamlTemplateLoader
from template.loader.csvloader import CsvTemplateLoader
from template.template_factory import TemplateFactory


class TestFactoryLoader(unittest.TestCase):
    """Test factory template loader"""

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_factory_loader_yaml(self):
        """Test factory YAML template loader"""
        with open('tests/test.yml', 'r', encoding='utf8') as file:
            factory = TemplateFactory(file)
            loader = factory.get_loader(file)
            self.assertEqual(loader.type, "YAML")
            self.assertIsInstance(loader, YamlTemplateLoader)
            info = factory.info
            self.assertEqual(info['template_type'], "YAML")
            self.assertEqual(info['loader'], "YamlTemplateLoader")

    def test_factory_loader_json(self):
        """Test factory JSON template loader"""
        with open('tests/test.json', 'r', encoding='utf8') as file:
            factory = TemplateFactory(file)
            loader = factory.get_loader(file)
            self.assertEqual(loader.type, "JSON")
            self.assertIsInstance(loader, JsonTemplateLoader)

    def test_factory_loader_csv(self):
        """Test factory CSV template loader"""
        with open('tests/test.csv', 'r', encoding='utf8') as file:
            factory = TemplateFactory(file)
            loader = factory.get_loader(file)
            self.assertEqual(loader.type, "CSV")
            self.assertIsInstance(loader, CsvTemplateLoader)

    def test_factory_loader_plaintext(self):
        """Test factory PlainText template loader"""
        with open('tests/test.txt', 'r', encoding='utf8') as file:
            factory = TemplateFactory(file)
            loader = factory.get_loader(file)
            self.assertEqual(loader.type, "PLAINTEXT")
            self.assertIsInstance(loader, PlainTextTemplateLoader)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
