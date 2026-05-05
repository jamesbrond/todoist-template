"""Test CSV template loader"""
import logging
import unittest
from template.loader.plaintextloader import PlainTextTemplateLoader


class TestPlainTextLoader(unittest.TestCase):
    """Test PlainText template loader"""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        loader = PlainTextTemplateLoader()
        with open('tests/test.txt', 'r', encoding='utf-8') as file:
            self.content = loader.load(file.read())

    def test_plaintext_load(self):
        """Test load PlainText"""
        self.assertTrue(self.content)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
