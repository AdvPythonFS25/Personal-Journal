import unittest
from entries.utils import count_entries_with_keyword

class TestCountEntriesWithKeyword(unittest.TestCase):

    def test_basic_match(self):
        entries = ["Today was great", "I had a bad day", "Great weather"]
        self.assertEqual(count_entries_with_keyword(entries, "great"), 2)

    def test_case_insensitivity(self):
        entries = ["Happy", "HAPPY", "hapPy"]
        self.assertEqual(count_entries_with_keyword(entries, "happy"), 3)

    def test_no_match(self):
        entries = ["One", "Two", "Three"]
        self.assertEqual(count_entries_with_keyword(entries, "four"), 0)

    def test_invalid_keyword(self):
        with self.assertRaises(ValueError):
            count_entries_with_keyword(["One", "Two"], 123)
