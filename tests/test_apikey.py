"""Test API topken storage"""
import os
import logging
import unittest
import keyring
from lib.config.apikey import EnvKeyring


class TestKeyring(unittest.TestCase):
    """Test API topken storage"""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.service = "FAKE_API_SERVICE"
        self.username = "API_TOKEN"
        self.token = "fake_token"

    def test_env_keyring_write(self):
        """Test API topken storage environment"""
        keyring.set_keyring(EnvKeyring())
        keyring.set_password(self.service, self.username, self.token)
        self.assertEqual(self.token, os.environ.get(self.service))

    def test_env_keyring_read(self):
        """Test API topken storage environment"""
        os.environ[self.service] = self.token
        keyring.set_keyring(EnvKeyring())
        token = keyring.get_password(self.service, self.username)
        self.assertEqual(self.token, token)

    def test_env_keyring_delete(self):
        """Test API topken storage environment"""
        keyring.set_keyring(EnvKeyring())
        keyring.delete_password(self.service, self.username)
        self.assertIs(os.environ.get(self.service), None)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
