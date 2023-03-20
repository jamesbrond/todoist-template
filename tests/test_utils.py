"""Test utils module"""
import logging
import unittest
from lib.utils import find_needle_in_haystack


class TestUtils(unittest.TestCase):
    """Test utils module"""

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.haystack = [
            {"id": 1, "name": "item1", "key": "key1"},
            {"id": 2, "name": "item2", "key": "key2"},
            {"id": 3, "name": "item3", "key": "key3"},
            {"id": 4, "name": "item4", "key": "key4"}
        ]

    def test_find_needle_in_haystack_mismatch_length(self):
        """Miasmatch length of needle and params"""
        self.assertEqual(find_needle_in_haystack([3], self.haystack, ["id", "key"]), None)

    def test_find_needle_in_haystack_success_1(self):
        """Search with 1 key"""
        item = find_needle_in_haystack([3], self.haystack, ["id"])
        self.assertEqual(item.get("name"), "item3")

    def test_find_needle_in_haystack_success_2(self):
        """Search with 2 keys"""
        item = find_needle_in_haystack([2, 'key2'], self.haystack, ["id", "key"])
        self.assertEqual(item.get("name"), "item2")
