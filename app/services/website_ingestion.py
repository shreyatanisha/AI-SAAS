
import requests
import re

from bs4 import BeautifulSoup

from urllib.parse import urljoin, urlparse, urldefrag

from collections import deque


def normalize_url(url: str):
    url = url.strip()

    # Remove URL fragments such as #contact
    url, _ = urldefrag(url)

    parsed = urlparse(url)

    # Remove trailing slash, except for the website root
    path = parsed.path.rstrip("/")

    if not path:
        path = "/"

    # Standardize the URL
    normalized_url = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=path
    ).geturl()

    return normalized_url

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

    excluded_extensions = (
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".svg", ".pdf", ".zip", ".mp4", ".mp3",
        ".css", ".js", ".ico"
    )

    for link in links:
        full_url = urljoin(base_url, link)
        parsed_url = urlparse(full_url)

        if (
            parsed_url.scheme in ("http", "https")
            and parsed_url.hostname == base_domain
            and not parsed_url.path.lower().endswith(excluded_extensions)
        ):
            internal_links.append(full_url)

    return internal_links
        
# ----------------------------------
# 4. EXTRACT TEXT FROM HTML
# ----------------------------------

def extract_text(html: str):

    soup = BeautifulSoup(html, "html.parser")

    unwanted_tags = [
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


def extract_contact_info(html: str):

    soup = BeautifulSoup(html, "html.parser")

    emails = set()
    phone_numbers = set()

    # Extract email and telephone links
    for link in soup.find_all("a", href=True):

        href = link["href"].strip()

        if href.lower().startswith("mailto:"):
            email = href[7:].split("?")[0].strip()
            if email:
                emails.add(email)

        elif href.lower().startswith("tel:"):
            phone = href[4:].strip()
            if phone:
                phone_numbers.add(phone)

    # Extract email addresses from visible website text
    page_text = soup.get_text(" ", strip=True)

    found_emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        page_text
    )

    emails.update(found_emails)

    # Extract phone numbers from visible website text
    found_phones = re.findall(
        r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)',
        page_text
    )

    phone_numbers.update(found_phones)

    return {
        "emails": sorted(emails),
        "phone_numbers": sorted(phone_numbers)
    }


def clean_text(text: str):

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


# ----------------------------------
# 5. CRAWL MULTIPLE WEBSITE PAGES
# ----------------------------------

def crawl_website(start_url: str, max_pages: int = None):

    queue = deque([normalize_url(start_url)])

    visited = set()

    pages_content = []

    while len(queue) > 0 and (max_pages is None or len(visited) < max_pages):

        current_url = normalize_url(queue.popleft())

        if current_url in visited:

            continue

        visited.add(current_url)

        print("Crawling:", current_url)

        try:
            html = fetch_page(current_url)
        except requests.RequestException as error:
            print(f"Failed to crawl {current_url}: {error}")
            continue

        title = extract_title(html)
        page_text = extract_text(html)
        cleaned_text = clean_text(page_text)

        # Extract contact information and add it to searchable content.
        contact_info = extract_contact_info(html)
        contact_text = ""

        if contact_info["emails"] or contact_info["phone_numbers"]:
            contact_text = "\n\nCompany Contact Information:\n"

            if contact_info["emails"]:
                contact_text += (
                    "Email Addresses: "
                    + ", ".join(contact_info["emails"])
                    + "\n"
                )

            if contact_info["phone_numbers"]:
                contact_text += (
                    "Phone Numbers: "
                    + ", ".join(contact_info["phone_numbers"])
                    + "\n"
                )

        final_content = cleaned_text + contact_text
        page_data = {
            "url": current_url,
            "title": title,
            "content": final_content,
            "source_type": "website",
        }
        pages_content.append(page_data)

        links = extract_links(html)
        internal_links = filter_internal_links(current_url, links)

        for link in internal_links:
            link = normalize_url(link)
            if link not in visited and link not in queue:
                queue.append(link)

    return pages_content
# ----------------------------------
# 6. TEST THE WEBSITE CRAWLER
# ----------------------------------

if __name__ == "__main__":

    start_url = "https://crushaderstech.com/"

    from app.vector_db.vector_store import store_document

    pages = crawl_website(start_url, max_pages=None)

    total_chunks = 0

    for page in pages:
        total_chunks += store_document(page)

    print("\nCrawling completed!")
    print("Maximum pages allowed: no limit")
    print("Total pages collected:", len(pages))
    print("Total chunks stored:", total_chunks)
