#!/usr/bin/env python3
import json
import unittest
from unittest.mock import patch, MagicMock
import librarian

class TestIsbnLookup(unittest.TestCase):

    def test_fetch_book_details_valid_isbn(self):
        result = librarian.fetch_book_details("9780760366950")
        self.assertIn("details", result)
        self.assertEqual(result["details"]["title"], "Motorcycle Safety Foundation's Guide to Motorcycling Excellence")


    def test_fetch_book_details_invalid_isbn(self):
        result = librarian.fetch_book_details("1234567891234")
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()