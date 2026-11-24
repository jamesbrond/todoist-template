"""Test factory template loader"""
import logging
from pathlib import Path
import pytest
from todoist_template.template.template_model import TTemplate
from todoist_template.template.loader.plaintextloader import PlainTextTemplateLoader
from todoist_template.template.loader.jsonloader import JsonTemplateLoader
from todoist_template.template.loader.yamlloader import YamlTemplateLoader
from todoist_template.template.loader.csvloader import CsvTemplateLoader
from todoist_template.template.template_factory import TemplateFactory


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


def test_factory_loader_yaml():
    """Test factory YAML template loader"""
    template: TTemplate = TTemplate(
        file=Path('tests/assets/test.yml'),
    )
    factory = TemplateFactory(template, keep_comments=False)
    loader = factory.template_loader
    assert loader.type == "YAML"
    assert factory.template_type == "YAML"
    assert isinstance(loader, YamlTemplateLoader)


def test_factory_loader_json():
    """Test factory JSON template loader"""
    template: TTemplate = TTemplate(
        file=Path('tests/assets/test.json'),
    )
    factory = TemplateFactory(template, keep_comments=False)
    loader = factory.template_loader
    assert loader.type == "JSON"
    assert isinstance(loader, JsonTemplateLoader)


def test_factory_loader_csv():
    """Test factory CSV template loader"""
    template: TTemplate = TTemplate(
        file=Path('tests/assets/test.csv'),
    )
    factory = TemplateFactory(template, keep_comments=False)
    loader = factory.template_loader
    assert loader.type == "CSV"
    assert isinstance(loader, CsvTemplateLoader)


def test_factory_loader_plaintext():
    """Test factory PlainText template loader"""
    template: TTemplate = TTemplate(
        file=Path('tests/assets/test.txt'),
    )
    factory = TemplateFactory(template, keep_comments=False)
    loader = factory.template_loader
    assert loader.type == "PLAINTEXT"
    assert isinstance(loader, PlainTextTemplateLoader)


# ~@:-]
