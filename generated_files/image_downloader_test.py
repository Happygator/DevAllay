# image_downloader_test.py

import unittest
from unittest.mock import patch, mock_open
from image_downloader import find_image_urls, download_images, find_next_page
import builtins

class TestImageDownloader(unittest.TestCase):

    @patch('requests.get')
    def test_find_image_urls(self, mock_get):
        # Test case for valid web page with jpeg images
        mock_get.return_value.text = '<img src="image1.jpg"><img src="image2.jpg">'
        urls = find_image_urls('http://example.com')
        self.assertEqual(urls, ['http://example.com/image1.jpg', 'http://example.com/image2.jpg'])

        # Test case for web page with relative image paths
        mock_get.return_value.text = '<img src="/images/image1.jpg"><img src="/images/image2.jpg">'
        urls = find_image_urls('http://example.com')
        self.assertEqual(urls, ['http://example.com/images/image1.jpg', 'http://example.com/images/image2.jpg'])

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_download_images(self, mock_print, mock_open, mock_get):
        # Test case for successful image download
        mock_get.return_value.content = b'fake image data'
        with patch('builtins.open', mock_open) as mock_file:
            download_images(['http://example.com/image1.jpg'], '/path/to/directory')
            mock_file.assert_called_once_with('/path/to/directory/image1.jpg', 'wb')
            mock_file().write.assert_called_once_with(b'fake image data')

        # Test case for failed image download
        mock_get.return_value.content = b''
        download_images(['http://example.com/image2.jpg'], '/path/to/directory')
        mock_print.assert_called_once_with('Failed to download image: http://example.com/image2.jpg')

    @patch('requests.get')
    def test_find_next_page(self, mock_get):
        # Test case for valid next page URL
        mock_get.return_value.text = '<a href="next_page.html">Next Link</a>'
        next_page = find_next_page('http://example.com')
        self.assertEqual(next_page, 'http://example.com/next_page.html')

        # Test case for missing "Next Link"
        mock_get.return_value.text = '<a href="previous_page.html">Previous Link</a>'
        next_page = find_next_page('http://example.com')
        self.assertIsNone(next_page)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
