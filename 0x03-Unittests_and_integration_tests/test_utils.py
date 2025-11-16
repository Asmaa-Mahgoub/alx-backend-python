#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as e1:
            access_nested_map({}, ("a",))
        self.assertEqual(str(e1.exception), "'a'")

        with self.assertRaises(KeyError) as e2:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(e2.exception), "'b'")


if __name__ == "__main__":
    unittest.main()




