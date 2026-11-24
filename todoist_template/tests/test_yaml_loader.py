"""Test YAML template loader"""
import logging
import pytest
from todoist_template.template.loader.yamlloader import YamlTemplateLoader


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def content():
    """Load the test YAML template"""
    loader = YamlTemplateLoader()
    with open('tests/assets/test.yml', 'r', encoding='utf-8') as file:
        return loader.load(file)


def test_yaml_load(content):
    """Test YAML template"""
    assert content
    assert len(content) == 1


def test_yaml_project_inbox(content):
    """Test YAML template Inbox"""
    assert 'Inbox' in content
    inbox = content['Inbox']
    assert len(inbox['tasks']) == 1


def test_yaml_task(content):
    """Test YAML template Inbox task"""
    tasks = content['Inbox']['tasks']
    assert tasks[0]['content'] == '🗑 delete {test_name|me} 🗑'


# ~@:-]
