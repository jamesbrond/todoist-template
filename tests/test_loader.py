"""Test factory template loader"""
import logging
from pathlib import Path
import unittest
from template.template_model import TTemplate
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
        template: TTemplate = TTemplate(
            file=Path('tests/test.yml'),
        )
        factory = TemplateFactory(template, keep_comments=False)
        loader = factory.template_loader
        self.assertEqual(loader.type, "YAML")
        self.assertEqual(factory.template_type, "YAML")
        self.assertTrue(isinstance(loader, YamlTemplateLoader))

    def test_factory_loader_json(self):
        """Test factory JSON template loader"""
        template: TTemplate = TTemplate(
            file=Path('tests/test.json'),
        )
        factory = TemplateFactory(template, keep_comments=False)
        loader = factory.template_loader
        self.assertEqual(loader.type, "JSON")
        self.assertIsInstance(loader, JsonTemplateLoader)

    def test_factory_loader_csv(self):
        """Test factory CSV template loader"""
        template: TTemplate = TTemplate(
            file=Path('tests/test.csv'),
        )
        factory = TemplateFactory(template, keep_comments=False)
        loader = factory.template_loader
        self.assertEqual(loader.type, "CSV")
        self.assertIsInstance(loader, CsvTemplateLoader)

    def test_factory_loader_plaintext(self):
        """Test factory PlainText template loader"""
        template: TTemplate = TTemplate(
            file=Path('tests/test.txt'),
        )
        factory = TemplateFactory(template, keep_comments=False)
        loader = factory.template_loader
        self.assertEqual(loader.type, "PLAINTEXT")
        self.assertIsInstance(loader, PlainTextTemplateLoader)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
