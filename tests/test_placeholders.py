"""Test placeholder replacement"""
import unittest
from lib.template import Template


class TestPlaceholders(unittest.TestCase):
    """Test placeholder replacement"""

    def setUp(self):
        self.placeholders = {
            "key1": "foo",
            "key2": "bar"
        }
        self.template = Template()

    def test_simple_replacement_not_string(self):
        """Simple replacement not string"""
        orig = 44
        self.assertEqual(self.template._replace(orig, self.placeholders), 44)

    def test_simple_replacement(self):
        """Simple replacement"""
        orig = "Test {key1}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test foo")

    def test_simple_replacement_with_fallback1(self):
        """Replacement with fallback 1"""
        orig = "Test {key1|not foo}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test foo")

    def test_simple_replacement_with_fallback2(self):
        """Replacement with fallback 2"""
        orig = "Test {key3|not foo}"
        self.assertEqual(self.template._replace(orig, self.placeholders), "Test not foo")

    def test_array(self):
        """Replacement in array"""
        orig = ["{key2}", "{key3|not foo}"]
        self.assertEqual(self.template._replace(orig, self.placeholders), ["bar", "not foo"])

    def test_dict(self):
        """Replacement in dict"""
        orig = {
            "id": 3,
            "name": "{key2}",
            "descr": "{key3|not foo}"
        }
        self.assertEqual(self.template._replace(orig, self.placeholders),
                         {"id": 3,
                          "name": "bar",
                          "descr": "not foo"})

# ~@:-]
