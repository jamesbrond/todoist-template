import logging
import unittest
from lib.loader.loaderfactory import TemplateLoaderFactory, JsonTemplateLoader, CsvTemplateLoader, YamlTemplateLoader



class TestFactoryLoader(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.factory = TemplateLoaderFactory()

    def test_factory_loader_yaml(self):
        loader = self.factory.get_loader('tests/test.yml')
        self.assertIsInstance(loader, YamlTemplateLoader)

    def test_factory_loader_json(self):
        loader = self.factory.get_loader('tests/test.json')
        self.assertIsInstance(loader, JsonTemplateLoader)

    def test_factory_loader_csv(self):
        loader = self.factory.get_loader('tests/test.csv')
        self.assertIsInstance(loader, CsvTemplateLoader)

    def test_factory_loader_not_supported(self):
        self.assertRaises(ValueError, self.factory.get_loader, 'tests/test.docx')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
