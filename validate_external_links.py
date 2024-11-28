"""
Purpose: Tool to detect broken external links on a website before it reaches production.

Note: treats a link as external if and only if it doesn't direct to a subpage of 'https://cloud.watonomous.ca/'
"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys


if len(sys.argv) < 2:
    print("Usage: python3 validate_external_links.py <BASE_URL> [WHITELISTED_URLS_PATH]")
    sys.exit(1)

WHITELISTED_URLS_PATH = None
if len(sys.argv) == 3:
    WHITELISTED_URLS_PATH = sys.argv[2]


BASE_URL = sys.argv[1]
INTERNAL_DEPLOYED_DOMAIN = 'https://cloud.watonomous.ca/'


def is_external_url(url):
    return not url.startswith(BASE_URL) and not url.startswith(INTERNAL_DEPLOYED_DOMAIN)


def is_down(url):
    return response.text

def check_broken_link(url):
    try:
        response = requests.get(url, allow_redirects=True)

        # Consider any 4xx or 5xx status code as a broken link
        if response.status_code == 401:
            print(f"{url} -- 401 Unauthorized")
        elif response.status_code == 403:
            print(f"{url} -- 403 Forbidden")
        elif response.status_code == 404:
            print(f"{url} -- 404 Page not found")
        elif response.status_code >= 400 and response.status_code < 500:
            print(f"{url} -- {response.status_code} Client error")
        elif response.status_code >= 500:
            print(f"{url} -- {response.status_code} Server error (possibly because of authentication)")
        else:
            print(f"{url} -- OK")
        return response.status_code >= 400

    except requests.RequestException:
        # Any error like connection issues or invalid URLs are treated as broken links
        print(f"{url} -- Request exception")
        return True
    
def get_links_on_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all anchor tags with href attributes
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Join relative URLs with the base URL to form complete links
        return [urljoin(url, link) for link in links]
    except requests.RequestException:
        print(f"Error fetching the page: {url}")


def parse_whitelisted_urls(urls_path):
    if not urls_path:
        return []

    with open(urls_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines



if __name__ == "__main__":

    whitelisted_urls = parse_whitelisted_urls(WHITELISTED_URLS_PATH)

    # ping Down Detector
    down_detector_online = False
    print("Pinging Down Detector")
    try:
        PING_DOWN_DETECTOR_API_URL = "https://downdetectorapi.com/v2/ping"
        response = requests.request("GET", PING_DOWN_DETECTOR_API_URL)
        if response.status_code == 200:
            down_detector_online = False
            print("Down Detector API OK")
        else:
            print("Down Detector API could not be reached")
    except:
        print("Down Detector API count not be reached")

    url = "https://downdetectorapi.com/v2/sites"
    headers = {'authorization': 'Bearer REPLACE_BEARER_TOKEN'}
    response = requests.request("GET", url, headers=headers)
    print(response.text)


    links = get_links_on_page(BASE_URL)
    external_links = [link for link in links if is_external_url(link)]
    for link in external_links:
        if is_broken_link(link):
            print(link)
        else:
            print("ok")


