#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""

import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct result"""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as error:
            utils.access_nested_map(nested_map, path)
        # Check that the exception message matches the missing key
        self.assertEqual(str(error.exception), f"'{path[-1]}'")


if __name__ == "__main__":
    unittest.main()
