#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
        @parameterized.expand([
             ({"a": 1},("a",)),
             ({"a": {"b": 2}},("a", "b")),
             ({"a": {"b": 2}},("a", "b"))
        ])
        def test_access_nested_map(self,nested_map, path, excepcted):
                        self.assertEqual(access_nested_map(nested_map,path), excepcted)
        
        @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
        def test_access_nested_map_exception(self, nested_map, path, expected):
            """ Test that a KeyError is raised for the respective inputs """
            with self.assertRaises(KeyError) as e:
                access_nested_map(nested_map, path)
            self.assertEqual(f"KeyError('{expected}')", repr(e.exception))

if __name__=="__main__":
    unittest.main()



