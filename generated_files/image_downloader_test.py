# image_downloader_test.py

import unittest
from unittest.mock import patch, mock_open
from image_downloader import find_image_urls, download_images, find_next_page_url, main

class TestImageDownloader(unittest.TestCase):

    @patch('image_downloader.requests.get')
    def test_find_image_urls_absolute_urls(self, mock_get):
        # Test finding image URLs with absolute URLs
        mock_get.return_value.text = '<img src="https://example.com/image1.jpg"><img src="https://example.com/image2.jpg">'
        urls = find_image_urls('https://example.com')
        self.assertEqual(urls, ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'])

    @patch('image_downloader.requests.get')
    def test_find_image_urls_relative_urls(self, mock_get):
        # Test finding image URLs with relative URLs
        mock_get.return_value.text = '<img src="/images/image1.jpg"><img src="/images/image2.jpg">'
        urls = find_image_urls('https://example.com')
        self.assertEqual(urls, ['https://example.com/images/image1.jpg', 'https://example.com/images/image2.jpg'])

    @patch('image_downloader.requests.get')
    def test_find_image_urls_no_images(self, mock_get):
        # Test finding image URLs when no images are present
        mock_get.return_value.text = '<p>No images found</p>'
        urls = find_image_urls('https://example.com')
        self.assertEqual(urls, [])

    @patch('image_downloader.requests.get')
    def test_download_images_success(self, mock_get):
        # Test successful image download
        image_urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
        with patch('builtins.open', mock_open()) as mock_file:
            download_images(image_urls, 'download_dir')
            mock_file.assert_called()

    @patch('image_downloader.requests.get')
    def test_download_images_failure(self, mock_get):
        # Test failed image download
        image_urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
        with patch('builtins.open', mock_open()) as mock_file:
            mock_get.side_effect = Exception('Failed to download')
            download_images(image_urls, 'download_dir')
            mock_file.assert_not_called()

    @patch('image_downloader.requests.get')
    def test_find_next_page_url_next_link_present(self, mock_get):
        # Test finding next page URL when "Next Link" is present
        mock_get.return_value.text = '<a href="https://example.com/page2">Next Link</a>'
        next_page_url = find_next_page_url('https://example.com/page1')
        self.assertEqual(next_page_url, 'https://example.com/page2')

    @patch('image_downloader.requests.get')
    def test_find_next_page_url_next_link_missing(self, mock_get):
        # Test finding next page URL when "Next Link" is missing
        mock_get.return_value.text = '<a href="https://example.com/page2">Previous Link</a>'
        next_page_url = find_next_page_url('https://example.com/page1')
        self.assertIsNone(next_page_url)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
