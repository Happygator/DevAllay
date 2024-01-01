```python
# image_downloader.py

#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import sys

def find_image_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img', src=True)
    image_urls = [urljoin(url, img['src']) for img in img_tags]
    return image_urls

def download_images(image_urls, directory):
    for image_url in image_urls:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            image_name = image_url.split('/')[-1]
            with open(os.path.join(directory, image_name), 'wb') as f:
                f.write(image_data)
        else:
            print(f'Failed to download image: {image_url}')

def find_next_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_link = soup.find('a', text='Next Link')
    if next_link:
        next_page_url = urljoin(url, next_link['href'])
        return next_page_url
    else:
        return None

def main():
    if len(sys.argv) != 2:
        print('Usage: ./image_downloader.py <first_web_page_url>')
        sys.exit(1)

    first_page_url = sys.argv[1]
    image_urls = []
    current_page_url = first_page_url

    while current_page_url:
        image_urls.extend(find_image_urls(current_page_url))
        current_page_url = find_next_page(current_page_url)

    download_images(image_urls, '/path/to/directory')

if __name__ == '__main__':
    main()
```

```python
# image_downloader_test.py

import unittest
from unittest.mock import patch, mock_open
from image_downloader import find_image_urls, download_images, find_next_page

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
        download_images(['http://example.com/image1.jpg'], '/path/to/directory')
        mock_open.assert_called_once_with('/path/to/directory/image1.jpg', 'wb')
        handle = mock_open()
        handle.write.assert_called_once_with(b'fake image data')

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
```