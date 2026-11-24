"""
Test KeyRing API Token Store
https://pypi.org/project/keyring/
"""
import keyring
import pytest
from todoist_template.config.apikey import EnvKeyring

TOKEN = "This is a test"


@pytest.fixture(autouse=True)
def _setup_keyring():
    """Ensure a usable keyring backend for tests"""
    if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
        keyring.set_keyring(EnvKeyring())
    yield


def test_keyring():
    """Test keyring set and get token using keyring"""

    keyring.set_password("TEST_KEYRING", "TEST", TOKEN)
    token = keyring.get_password("TEST_KEYRING", "TEST")
    assert token == TOKEN


def test_retrieve_from_keyring():
    """Test retrieve token from KeyRing"""

    token = keyring.get_password("TEST_KEYRING", "TEST")
    assert token == TOKEN


# ~@:-]
