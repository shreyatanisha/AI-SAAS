import requests     #allows python to send HTTP requests to websites so that it will send its webpage
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque   #collection is a built-in Python module. and deque is a data structure that lets us efficiently add and remove items from either end.


def fetch_page(url: str):

    response = requests.get(
        url,
        headers={"User-Agent": "AI-SAAS website ingestion/1.0"},
        timeout=15
    )
    response.raise_for_status()
    
    return response.text


def extract_links(html: str):

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", href=True)

    urls = []

    for link in links:

        url = link["href"]

        urls.append(url)

    return urls


def filter_internal_links(base_url: str, links: list):

    internal_links = []

    base_domain = urlparse(base_url).hostname

    for link in links:

        full_url = urljoin(base_url, link)

        parsed_url = urlparse(full_url)

        if (
            parsed_url.scheme in ("http", "https")
            and parsed_url.hostname == base_domain
        ):

            internal_links.append(full_url)

    return internal_links


if __name__ == "__main__":

    start_url = "https://crushaderstech.com/"

    queue = deque([start_url])

    visited = set()

    while len(queue) > 0:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        print("Crawling:", current_url)

        html = fetch_page(current_url)

        links = extract_links(html)

        internal_links = filter_internal_links(
            start_url,
            links
        )

        for link in internal_links:

            if link not in visited:

                if link not in queue:

                    queue.append(link)

    print("\nCrawling completed!")

    print("Total pages visited:", len(visited))

   









