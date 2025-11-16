#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
    ({}, ("a",)),
    ({"a": 1}, ("a", "b")),
])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected JSON payload."""
        # Create a mock response with .json() returning test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get so no real HTTP call is made
        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)

            # Ensure requests.get was called exactly once with the URL
            mock_get.assert_called_once_with(test_url)

            # Ensure get_json returns the payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator."""

    def test_memoize(self):
        """Test memoize caches method result."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            first = obj.a_property
            second = obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()




