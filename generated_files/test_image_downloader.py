# test_image_downloader.py

import unittest
from unittest.mock import patch, MagicMock
from image_downloader import download_images, find_image_url, find_next_page_url

class TestImageDownloader(unittest.TestCase):

    @patch('image_downloader.requests.get')
    def test_download_images(self, mock_get):
        # Test case for successful download of images from multiple pages
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><img src='image1.jpg'><a href='next_page'>Next Link</a></html>"
        mock_get.return_value = mock_response

        with patch('image_downloader.find_image_url', return_value='http://example.com/image1.jpg'):
            with patch('image_downloader.find_next_page_url', return_value='http://example.com/next_page'):
                download_images('http://example.com/first_page')

        # Assert that the download_images function makes the correct number of calls to find_image_url and find_next_page_url
        self.assertEqual(mock_get.call_count, 2)

    def test_find_image_url(self):
        # Test case for finding absolute image URL from relative path
        page_content = "<html><img src='image.jpg'></html>"
        base_url = 'http://example.com/'
        absolute_url = find_image_url(page_content, base_url)
        self.assertEqual(absolute_url, 'http://example.com/image.jpg')

    def test_find_next_page_url(self):
        # Test case for finding absolute URL of the next page
        page_content = "<html><a href='next_page'>Next Link</a></html>"
        base_url = 'http://example.com/'
        next_page_url = find_next_page_url(page_content, base_url)
        self.assertEqual(next_page_url, 'http://example.com/next_page')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
