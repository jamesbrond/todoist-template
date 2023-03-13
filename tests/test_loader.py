"""Test factory template loader"""
import logging
import unittest
from lib.loader.loaderfactory import TemplateLoaderFactory, JsonTemplateLoader, CsvTemplateLoader, YamlTemplateLoader


class TestFactoryLoader(unittest.TestCase):
    """Test factory template loader"""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.factory = TemplateLoaderFactory()

    def test_factory_loader_yaml(self):
        """Test factory YAML template loader"""
        loader = self.factory.get_loader('tests/test.yml')
        self.assertIsInstance(loader, YamlTemplateLoader)

    def test_factory_loader_json(self):
        """Test factory JSON template loader"""
        loader = self.factory.get_loader('tests/test.json')
        self.assertIsInstance(loader, JsonTemplateLoader)

    def test_factory_loader_csv(self):
        """Test factory CSV template loader"""
        loader = self.factory.get_loader('tests/test.csv')
        self.assertIsInstance(loader, CsvTemplateLoader)

    def test_factory_loader_not_supported(self):
        """Test factory not supported template loader"""
        self.assertRaises(ValueError, self.factory.get_loader, 'tests/test.docx')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
