"""Test CSV template loader"""
import logging
import pytest
from todoist_template.template.loader.plaintextloader import PlainTextTemplateLoader


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def content():
    """Load the test plaintext template"""
    loader = PlainTextTemplateLoader()
    with open('tests/assets/test.txt', 'r', encoding='utf-8') as file:
        return loader.load(file.read())


def test_plaintext_load(content):
    """Test load PlainText"""
    assert content


# ~@:-]
