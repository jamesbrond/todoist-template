"""
Test KeyRing API Token Store
https://pypi.org/project/keyring/
"""
import unittest
import keyring
from config.apikey import EnvKeyring


class TestKeyRingAPI(unittest.TestCase):
    """Test KeyRing API Token Store"""

    def setUp(self):
        self.token = "This is a test"

        if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
            keyring.set_keyring(EnvKeyring())

    def test_keyring(self):
        """Test keyring set and get token using keyring"""

        keyring.set_password("TEST_KEYRING", "TEST", self.token)
        token = keyring.get_password("TEST_KEYRING", "TEST")
        self.assertEqual(token, self.token)

    def test_retrieve_from_keyring(self):
        """Test retrieve token from KeyRing"""

        token = keyring.get_password("TEST_KEYRING", "TEST")
        self.assertEqual(token, self.token)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
