"""Test factory template loader"""
import logging
import unittest
from lib.loader.loaderfactory import TemplateLoaderFactory, JsonTemplateLoader, CsvTemplateLoader, YamlTemplateLoader


class TestFactoryLoader(unittest.TestCase):
    """Test factory template loader"""

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_factory_loader_yaml(self):
        """Test factory YAML template loader"""
        with open('tests/test.yml', 'r', encoding='utf8') as file:
            factory = TemplateLoaderFactory(file)
            loader = factory.get_loader(file)
            self.assertIsInstance(loader, YamlTemplateLoader)

    def test_factory_loader_json(self):
        """Test factory JSON template loader"""
        with open('tests/test.json', 'r', encoding='utf8') as file:
            factory = TemplateLoaderFactory(file)
            loader = factory.get_loader(file)
            self.assertIsInstance(loader, JsonTemplateLoader)

    def test_factory_loader_csv(self):
        """Test factory CSV template loader"""
        with open('tests/test.csv', 'r', encoding='utf8') as file:
            factory = TemplateLoaderFactory(file)
            loader = factory.get_loader(file)
            self.assertIsInstance(loader, CsvTemplateLoader)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
