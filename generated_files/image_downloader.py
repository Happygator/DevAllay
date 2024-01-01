# image_downloader.py

#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urljoin  # Import urljoin function

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
    next_link = soup.find('a', string='Next Link')  # Replace 'text' with 'string'
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
