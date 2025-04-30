# backend/crawler.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import uuid
import zipfile

from backend.analyzer import extract_page_data
from backend.report_generator import generate_excel_report

def is_valid_link(href, base_url):
    if not href:
        return False
    parsed = urlparse(href)
    return (
        not parsed.scheme or parsed.netloc == urlparse(base_url).netloc
    )

def crawl_site(start_url):
    visited = set()
    to_visit = [start_url]
    pages = []
    session_id = str(uuid.uuid4())[:8]
    output_dir = f"output_{session_id}"
    os.makedirs(output_dir, exist_ok=True)

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text()
            page_lang = "unknown"

            try:
                from langdetect import detect
                if len(text.strip()) > 20:
                    page_lang = detect(text)
            except:
                pass

            lang_dir = os.path.join(output_dir, page_lang)
            os.makedirs(lang_dir, exist_ok=True)

            page_title = soup.title.string.strip() if soup.title else "page"
            filename = f"{page_title[:80].replace('/', '_')}_{len(visited)+1}.html"
            filepath = os.path.join(lang_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(res.text)

            pages.append({
                "url": url,
                "html": res.text,
                "lang": page_lang
            })

            visited.add(url)

            for link in soup.find_all("a", href=True):
                full_link = urljoin(url, link['href'])
                if is_valid_link(full_link, start_url) and full_link not in visited:
                    to_visit.append(full_link)

        except Exception as e:
            print(f"[ERROR] Skipping {url}: {e}")

    return pages, output_dir

def analyze_and_report(pages, output_dir, website_name):
    data_by_lang = defaultdict(list)

    for idx, page in enumerate(pages, 1):
        data = extract_page_data(
            html_content=page["html"],
            page_url=page["url"],
            counter=idx
        )
        data_by_lang[page["lang"]].append(data)

    report_path = os.path.join(output_dir, f"website_{website_name}_Scrapy.xlsx")
    generate_excel_report(data_by_lang, report_path)
    return report_path

def zip_all_languages(base_output_dir):
    combined_zip = os.path.join(base_output_dir, "all_languages_html.zip")
    with zipfile.ZipFile(combined_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(base_output_dir):
            for file in files:
                if file.endswith(".html"):
                    full_path = os.path.join(root, file)
                    arc
