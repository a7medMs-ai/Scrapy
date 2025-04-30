# backend/analyzer.py

from bs4 import BeautifulSoup
import re
from langdetect import detect


def count_words(text):
    words = re.findall(r'\w+', text, re.UNICODE)
    return len(words)


def count_segments(soup):
    segment_tags = ['p', 'li', 'div', 'span', 'section', 'article']
    segments = []
    for tag in segment_tags:
        segments.extend(soup.find_all(tag))
    return len(segments)


def has_media(soup):
    return bool(soup.find(['img', 'video', 'audio', 'iframe']))


def extract_full_text(soup):
    # Remove script and style elements
    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.extract()
    return soup.get_text(separator=' ', strip=True)


def extract_page_data(html_content: str, page_url: str, counter: int = 1):
    soup = BeautifulSoup(html_content, "html.parser")
    page_name = soup.title.string.strip() if soup.title else f"Page_{counter}"
    full_text = extract_full_text(soup)

    data = {
        "Page Counter": counter,
        "Page Name": page_name[:100],
        "Word Count": count_words(full_text),
        "Segments": count_segments(soup),
        "Has Media": has_media(soup),
        "URL": page_url,
        "Full Content": full_text[:30000],  # Excel-safe limit
        "Language": detect(full_text) if len(full_text) >= 20 else "unknown",
    }

    return data
