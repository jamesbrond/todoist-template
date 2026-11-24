"""Test CSV template loader"""
import logging
import pytest
from todoist_template.template.loader.csvloader import CsvTemplateLoader


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def content():
    """Load the test CSV template"""
    loader = CsvTemplateLoader()
    with open('tests/assets/test.csv', 'r', encoding='utf-8') as file:
        return loader.load(file.read())


def test_csv_load(content):
    """Test load CSV"""
    assert content
    assert len(content) == 2


def test_csv_project_0_inbox(content):
    """Test load CSV project"""
    assert 'Inbox' in content[0]
    inbox = content[0]['Inbox']
    assert len(inbox['tasks']) == 1


def test_csv_project_1_test_project(content):
    """Test load CSV project task"""
    assert 'Test project' in content[1]
    prj = content[1]['Test project']
    assert len(prj['tasks']) == 0


def test_csv_section(content):
    """Test load CSV session"""
    assert 'Test section' in content[1]
    sec = content[1]['Test section']
    assert len(sec['tasks']) == 2


def test_csv_task(content):
    """Test load CSV session task"""
    tasks = content[1]['Test section']['tasks']
    assert tasks[0]['content'] == 'Test task 1'
    assert tasks[0]['labels'] == ['label3', 'label4']


# ~@:-]
