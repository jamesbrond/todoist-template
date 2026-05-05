"""
Test KeyRing API Token Store
https://pypi.org/project/keyring/
"""
import unittest
import keyring


class TestKeyRingAPI(unittest.TestCase):
    """Test KeyRing API Token Store"""

    def setUp(self):
        self.TOKEN = "This is a test"

        if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
            from lib.config.apikey import EnvKeyring
            keyring.set_keyring(EnvKeyring())

    def test_keyring(self):
        """Test keyring set and get token using keyring"""

        keyring.set_password("TEST_KEYRING", "TEST", self.TOKEN)
        token = keyring.get_password("TEST_KEYRING", "TEST")
        self.assertEqual(token, self.TOKEN)

    def test_retrieve_from_keyring(self):
        """Test retrieve token from KeyRing"""

        token = keyring.get_password("TEST_KEYRING", "TEST")
        self.assertEqual(token, self.TOKEN)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
