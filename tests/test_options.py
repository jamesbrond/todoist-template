"""Test Config class"""
import unittest
from lib.config.config import TTOptions


class TestTTOptions(unittest.TestCase):
    """Test Options class"""

    def setUp(self):
        self.plain = TTOptions({"key0": "value0", "key1": "value1"})
        self.nested = TTOptions({
            "parent0": {
                "child0": "value0",
                "child1": "value1"
            },
            "parent1": {
                "child2": "value2",
                "child3": "value3"
            }})

    def test_constructor_none(self):
        """TTOptions contructor no arguments"""
        self.assertEqual(len(TTOptions()), 0)
        self.assertEqual(len(TTOptions({})), 0)

    def test_constructor_kwargs(self):
        """TTOptions contructor kwargs"""
        self.assertEqual(len(TTOptions(key0="value0")), 1)
        self.assertEqual(len(TTOptions(leaf="value0", parent={"child": "value"})), 2)

    def test_constructor_scalar(self):
        """TTOptions contructor scalar argument"""
        with self.assertRaises(ValueError):
            TTOptions("test")
        with self.assertRaises(ValueError):
            TTOptions({"test"})

    def test_constructor_array(self):
        """TTOptions contructor array argument"""
        with self.assertRaises(ValueError):
            TTOptions(["test"])

    def test_constructor_plain_dict(self):
        """TTOptions contructor plain dict argument"""
        self.assertEqual(len(self.plain), 2)
        self.assertEqual(self.plain.key1, "value1")

    def test_constructor_nested_dict(self):
        """TTOptions contructor nested dict argument"""
        self.assertEqual(len(self.nested), 2)
        self.assertIsInstance(self.nested.parent0, TTOptions)
        self.assertEqual(self.nested.parent1.child2, "value2")

    def test_options_set(self):
        """TTOptions option set"""
        self.plain.key1 = "new_value1"
        self.assertEqual(len(self.plain), 2)
        self.assertEqual(self.plain.key1, "new_value1")

        self.nested.parent1.child2 = "new_value2"
        self.assertEqual(len(self.nested), 2)
        self.assertIsInstance(self.nested.parent1, TTOptions)
        self.assertEqual(self.nested.parent1.child2, "new_value2")

    def test_options_setattr(self):
        """TTOptions option setattr"""
        self.plain.set("key1", 6)
        self.assertEqual(len(self.plain), 2)
        self.assertEqual(self.plain.key1, 6)

        self.nested.set("parent1.child2", "new_value2")
        self.assertEqual(len(self.nested), 2)
        self.assertIsInstance(self.nested.parent1, TTOptions)
        self.assertEqual(self.nested.parent1.child2, "new_value2")

        self.nested.set("parent2.child4", "new_value4")
        self.assertEqual(len(self.nested), 3)
        self.assertIsInstance(self.nested.parent2, TTOptions)
        self.assertEqual(self.nested.parent2.child4, "new_value4")

    def test_options_del_leaf(self):
        """TTOptions option del leaf"""
        del self.plain.key1
        self.assertEqual(len(self.plain), 1)
        self.assertFalse(self.plain.key1)

        del self.nested.parent1.child2
        self.assertEqual(len(self.nested), 2)
        self.assertIsInstance(self.nested.parent1, TTOptions)
        self.assertEqual(len(self.nested.parent1), 1)
        self.assertFalse(self.nested.parent1.child2)

    def test_options_del_parent(self):
        """TTOptions option del parent"""
        del self.nested.parent1
        self.assertEqual(len(self.nested), 1)
        self.assertIsInstance(self.nested.parent0, TTOptions)
        self.assertFalse(self.nested.parent1)

    def test_update(self):
        """TTOptions update with dict"""
        new_value = {
            "parent0": {
                "child0": "value0",
                "child1": "new_value1"
            },
            "parent1": {
                "child3": "new_value3",
                "child4": 4
            },
            "key0": [1, 2, 3, 4]}
        self.nested.update(new_value)
        self.assertEqual(len(self.nested), 3)
        self.assertIsInstance(self.nested.parent0, TTOptions)
        self.assertIsInstance(self.nested.parent1, TTOptions)
        self.assertEqual(self.nested.key0[0], 1)

    def test_update_with_option(self):
        """TTOptions update with TTOptions"""
        new_nested = TTOptions({
            "parent0": {
                "child0": "value0",
                "child1": "new_value1"
            },
            "parent1": {
                "child3": "new_value3",
                "child4": 4
            },
            "key0": [1, 2, 3, 4]})
        self.nested.update(new_nested)
        self.assertEqual(len(self.nested), 3)
        self.assertIsInstance(self.nested.parent0, TTOptions)
        self.assertIsInstance(self.nested.parent1, TTOptions)
        self.assertEqual(self.nested.key0[0], 1)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
