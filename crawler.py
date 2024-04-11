import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import xml.etree.ElementTree as ET

def crawl_sitemap_for_urls(sitemap_url, contains_string):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(sitemap_url)
        if response.status_code != 200:
            print(f"Failed to fetch sitemap: HTTP {response.status_code}")
            return []
        
    root = ET.fromstring(response.content)
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [elem.text for elem in root.findall('.//ns:loc', namespaces=namespaces)]
    filtered_urls = [url for url in urls if contains_string in url]

    return filtered_urls

# Example usage
sitemap_url = "https://thestreameast.to/sitemap.xml"  # Replace with the actual sitemap URL
contains_string = "baltimore-orioles"  # Replace with the substring you're looking for in the URLs

filtered_urls = crawl_sitemap_for_urls(sitemap_url, contains_string)
for url in filtered_urls:
    print(url)

