import re
import time
import json
import requests
from concurrent import futures
import os

g_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
}

def bing_get_image_url_using_api(keywords, max_number=10000, face_only=False):
    start = 1
    image_urls = []
    while start <= max_number:
        url = 'https://www.bing.com/images/async?q={}&first={}&count=35'.format(keywords, start)
        res = requests.get(url, headers=g_headers)
        res.encoding = "utf-8"
        image_urls_batch = re.findall('murl&quot;:&quot;(.*?)&quot;', res.text)
        if len(image_urls) > 0 and image_urls_batch[-1] == image_urls[-1]:
            break
        image_urls += image_urls_batch
        start += len(image_urls_batch)
    return image_urls

def crawl_image_urls(keywords, engine="Bing", max_number=10000,
                     face_only=False, quiet=False, browser="api"):
    print("\nScraping From {} Image Search ...\n".format(engine))
    print("Keywords:  " + keywords)
    
    if max_number <= 0:
        print("Number:  No limit")
        max_number = 10000
    else:
        print("Number:  {}".format(max_number))
    
    print("Face Only:  {}".format(str(face_only)))
    
    if engine == "Bing" and browser == "api":
        image_urls = bing_get_image_url_using_api(keywords, max_number=max_number, face_only=face_only)
    else:
        print("The specified combination of engine and browser is not supported.")
        return []

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    print("\n== {0} out of {1} crawled images URLs will be used.\n".format(
        output_num, len(image_urls)))

    return image_urls[0:output_num]

# Example usage:
keywords = "Chris Hemsworth and Chris Evans"
engine = "Bing"
max_number = 10  # Set your desired maximum number of image URLs
face_only = True
quiet = False
browser = "api"  # Use the API method for Bing

image_urls = crawl_image_urls(keywords, engine, max_number, face_only, quiet, browser)
# You can now use the 'image_urls' list for your needs.

# Create a directory to save the downloaded images
save_dir = "downloaded_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    
    
headers_response = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept": "image/jpeg"
}    

# Iterate through the image URLs and download each image
for i, image_url in enumerate(image_urls):
    try:
        response = requests.get(image_url, headers=headers_response)
        if response.status_code == 200:
            # Generate a unique filename for each image
            filename = os.path.join(save_dir, f"image_{i + 1}.jpg")

            # Save the image to the specified directory
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download image {i + 1}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading image {i + 1}: {str(e)}")

print("Download completed.")

