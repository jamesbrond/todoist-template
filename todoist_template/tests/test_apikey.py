"""Test API topken storage"""
import os
import logging
import keyring
import pytest
from todoist_template.config.apikey import EnvKeyring

SERVICE = "FAKE_API_SERVICE"
USERNAME = "API_TOKEN"
TOKEN = "fake_token"


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


def test_env_keyring_write():
    """Test to write API topken in storage environment"""
    keyring.set_keyring(EnvKeyring())
    keyring.set_password(SERVICE, USERNAME, TOKEN)
    assert os.environ.get(SERVICE) == TOKEN


def test_env_keyring_read():
    """Test to read API topken from storage environment"""
    os.environ[SERVICE] = TOKEN
    keyring.set_keyring(EnvKeyring())
    token = keyring.get_password(SERVICE, USERNAME)
    assert token == TOKEN


def test_env_keyring_delete():
    """Test to delete API topken from storage environment"""
    keyring.set_keyring(EnvKeyring())
    keyring.delete_password(SERVICE, USERNAME)
    assert os.environ.get(SERVICE) is None


# ~@:-]
