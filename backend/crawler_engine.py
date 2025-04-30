# backend/crawler_engine.py

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import pandas as pd
import zipfile
import uuid

from backend.analyzer import extract_page_data
from backend.report_generator import generate_excel_report


def is_valid_link(href, base_url):
    if not href:
        return False
    parsed = urlparse(href)
    return (
        not parsed.scheme or parsed.netloc == urlparse(base_url).netloc
    )


def crawl_site(start_url, lang_code="en", max_pages=100):
    visited = set()
    to_visit = [start_url]
    html_pages = []
    session_id = str(uuid.uuid4())[:8]
    output_dir = f"output_{session_id}/{lang_code}"
    os.makedirs(output_dir, exist_ok=True)

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            filename = soup.title.string.strip() if soup.title else "page"
            filename = filename.replace("/", "_").replace("\\", "_")[:100]
            filename = f"{filename}_{len(visited)+1}.html"

            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(res.text)

            html_pages.append({
                "url": url,
                "filepath": filepath,
                "html": res.text
            })

            visited.add(url)

            for link in soup.find_all("a", href=True):
                full_link = urljoin(url, link['href'])
                if is_valid_link(full_link, start_url) and full_link not in visited:
                    to_visit.append(full_link)

        except Exception as e:
            print(f"Error crawling {url}: {e}")
            continue

    return html_pages, output_dir


def analyze_and_report(html_pages, output_dir, website_name, lang_code):
    report_data = []
    for idx, page in enumerate(html_pages, 1):
        data = extract_page_data(
            html_content=page["html"],
            page_url=page["url"],
            counter=idx
        )
        report_data.append(data)

    report_path = os.path.join(
        output_dir,
        f"website_{website_name}_Scrapy.xlsx"
    )

    generate_excel_report(report_data, report_path, lang_code)
    return report_path


def zip_pages_by_language(base_output_dir, lang_code):
    zip_name = os.path.join(base_output_dir, f"{lang_code}_html_pages.zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(os.path.join(base_output_dir, lang_code)):
            for file in files:
                zipf.write(os.path.join(root, file),
                           arcname=os.path.relpath(os.path.join(root, file), base_output_dir))
    return zip_name


def process_site(url, lang_code="en", max_pages=100):
    # Extract domain for naming
    website_name = urlparse(url).netloc.replace("www.", "").split(".")[0]

    # Crawl
    html_pages, output_dir = crawl_site(url, lang_code=lang_code, max_pages=max_pages)

    # Analyze + Report
    report_path = analyze_and_report(html_pages, output_dir, website_name, lang_code)

    # Zip files
    zip_path = zip_pages_by_language(output_dir, lang_code)

    return report_path, zip_path, output_dir
