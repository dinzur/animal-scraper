import sys
import os
import unittest

# Add src/ to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scraper import extract_adjective_animal_map

class TestScraper(unittest.TestCase):

    def test_extraction_returns_dict(self):
        result = extract_adjective_animal_map()
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

    def test_common_animal_exists(self):
        result = extract_adjective_animal_map()
        all_animals = [animal for animals in result.values() for animal in animals]
        self.assertIn("lion", [a.lower() for a in all_animals])

if __name__ == '__main__':
    unittest.main()
