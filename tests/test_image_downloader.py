import sys
import os
import unittest
from unittest.mock import patch, Mock

# Add src/ to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from image_downloader import download_and_save_image

class TestImageDownloader(unittest.TestCase):

    @patch('image_downloader.requests.get')
    def test_download_and_save_image(self, mock_get):
        mock_response = Mock()
        mock_response.content = b'fakeimagebytes' * 1024  # >2048 bytes
        mock_response.headers = {'Content-Type': 'image/jpeg'}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        from bs4 import BeautifulSoup
        img_tag = BeautifulSoup('<img src="//upload.wikimedia.org/fake.jpg">', 'html.parser').img
        filename = download_and_save_image(img_tag, "test_animal")

        self.assertTrue(os.path.exists(filename))
        os.remove(filename)  # Clean up

if __name__ == '__main__':
    unittest.main()
