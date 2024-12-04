"""
Purpose: Tool to detect broken external links on a website before it
reaches production. Whitelisted URLs are ignored. Write whitelisted
URLs in a file, one per line.

Note: treats a link as external if and only if it doesn't direct to a subpage
of 'https://cloud.watonomous.ca/'

"Usage: python3 validate_external_links.py <BASE_URL> [WHITELISTED_URLS_PATH]"
"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import typing


if len(sys.argv) < 2:
    print("Usage: python3 validate-external-links.py <BASE_URL> [WHITELISTED_URLS_PATH]")
    sys.exit(1)

WHITELISTED_URLS_PATH = None
if len(sys.argv) == 3:
    WHITELISTED_URLS_PATH = sys.argv[2]


URL = sys.argv[1]
INTERNAL_DEPLOYED_DOMAIN = 'https://cloud.watonomous.ca/'


def is_external_url(url):
    return not url.startswith(URL) and not url.startswith(INTERNAL_DEPLOYED_DOMAIN)


def link_ok(url: str) -> (str, bool):
    try:
        response = requests.get(url, allow_redirects=False)

        # Consider any 4xx or 5xx status code as a broken link
        # 3xx Redirects are NOT considered broken

        if response.status_code == 401:
            return f"{response.status_code} Unauthorized -- {url}", False
        elif response.status_code == 403:
            return f"{response.status_code} Forbidden -- {url}", False
        elif response.status_code == 404:
            return f"{response.status_code} Page not found -- {url}", False
        elif response.status_code >= 400 and response.status_code < 500:
            return f"{response.status_code} Client error -- {url}", False
        elif response.status_code >= 500:
            return f"{response.status_code} Server error " + \
                f"(possibly because of authentication) -- {url}", False
        else:
            return f"OK -- {url}", True

    except requests.RequestException:
        # Any error like connection issues or invalid URLs are treated as broken links
        return f"{url} -- Request exception", False
    
def get_links_on_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all anchor tags with href attributes
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    # Join relative URLs with the base URL to form complete links
    return [urljoin(url, link) for link in links]


def parse_whitelisted_urls(urls_path):
    if not urls_path:
        return []

    with open(urls_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines



if __name__ == "__main__":
    whitelisted_urls = parse_whitelisted_urls(WHITELISTED_URLS_PATH)
    links = get_links_on_page(URL)
    external_links = [link for link in links if is_external_url(link)]

    broken_count = 0
    whitelist_ignores_count = 0
    for link in external_links:
        result, ok = link_ok(link)
        if ok:
            continue
        if link in whitelisted_urls:
            whitelist_ignores_count += 1
            continue

        broken_count += 1
        print(result)

    print("DONE")
    print(f"{len(links)} external links in total")
    print(f"{whitelist_ignores_count} broken whitelisted links ignored")
    print(f"{broken_count} broken links")





