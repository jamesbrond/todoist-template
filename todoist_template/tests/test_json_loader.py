"""Test JSON template loader"""
import logging
import pytest
from todoist_template.template.loader.jsonloader import JsonTemplateLoader


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def content():
    """Load the test JSON template"""
    loader = JsonTemplateLoader()
    with open('tests/assets/test.json', 'r', encoding='utf-8') as file:
        return loader.load(file.read())


def test_json_load(content):
    """Test JSON template loader"""
    assert content


def test_json_project_inbox(content):
    """Test JSON template Inbox"""
    assert 'Inbox' in content
    inbox = content['Inbox']
    assert len(inbox['tasks']) == 1


def test_json_task(content):
    """Test JSON template Inbox task"""
    tasks = content['Inbox']['tasks']
    assert tasks[0]['content'] == 'delete me'


# ~@:-]
