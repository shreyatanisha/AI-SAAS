
import requests
import re

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse

from collections import deque


# ----------------------------------
# 1. DOWNLOAD A WEBPAGE
# ----------------------------------

def fetch_page(url: str):

    url = url.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",

        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return response.text


# ----------------------------------
# 2. EXTRACT LINKS FROM HTML
# ----------------------------------

def extract_links(html: str):

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", href=True)

    urls = []

    for link in links:

        url = link["href"]

        urls.append(url)

    return urls


# ----------------------------------
# 3. FILTER INTERNAL LINKS
# ----------------------------------

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


# ----------------------------------
# 4. EXTRACT TEXT FROM HTML
# ----------------------------------

def extract_text(html: str):

    soup = BeautifulSoup(html, "html.parser")

    unwanted_tags = [
        "nav",
        "footer",
        "script",
        "style"
    ]

    for tag in unwanted_tags:

        for element in soup.find_all(tag):

            element.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text

def extract_title(html: str):

    soup = BeautifulSoup(html, "html.parser")

    if soup.title:

        return soup.title.get_text(strip=True)

    return "Untitled Page"

def clean_text(text: str):

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


# ----------------------------------
# 5. CRAWL MULTIPLE WEBSITE PAGES
# ----------------------------------

def crawl_website(start_url: str, max_pages: int = 10):

    queue = deque([start_url])

    visited = set()

    pages_content = []

    while len(queue) > 0 and len(visited) < max_pages:

        current_url = queue.popleft()

        if current_url in visited:

            continue

        visited.add(current_url)

        print("Crawling:", current_url)

        html = fetch_page(current_url)

        title = extract_title(html)

        page_text = extract_text(html)

        cleaned_text = clean_text(page_text)

        page_data = {
           "url": current_url,
           "title": title,
           "content": cleaned_text,
           "source_type": "website"
        }

        pages_content.append(page_data)

        links = extract_links(html)

        internal_links = filter_internal_links(
          current_url,
          links
        )
        

        for link in internal_links:

            if link not in visited:

                if link not in queue:

                    queue.append(link)

    return pages_content


# ----------------------------------
# 6. TEST THE WEBSITE CRAWLER
# ----------------------------------

if __name__ == "__main__":

    start_url = "https://crushaderstech.com/"

    max_pages = 10

    pages_content = crawl_website(
        start_url,
        max_pages
    )

    print("\nCrawling completed!")

    print("Maximum pages allowed:", max_pages)

    print("Total pages collected:", len(pages_content))

    print("\nExtracted Website Content:")

    for page in pages_content:

      print("Source URL:", page["url"])
    
      print("Page Title:", page["title"])

      print("Content:", page["content"])

      print("--------------------")
        
        
# if __name__ == "__main__":

#     sample_text = """
#         Welcome     to     ABC Company.


#         We provide       web development
#         services.
#     """

#     cleaned_text = clean_text(sample_text)

#     print("Original Text:")
#     print(sample_text)

#     print("\nCleaned Text:")
#     print(cleaned_text)
