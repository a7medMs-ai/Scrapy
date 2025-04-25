import scrapy
import os
from bs4 import BeautifulSoup
from langdetect import detect
from urllib.parse import urlparse, urljoin
from pathlib import Path

class MultilingualSpider(scrapy.Spider):
    name = "multilingual_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("start_url is required to start crawling.")
        self.start_urls = [start_url]
        self.visited_urls = set()
        self.base_domain = urlparse(start_url).netloc
        self.file_names = {}

    def clean_filename(self, name):
        name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()
        return name[:80]

    def unique_filename(self, base_name):
        base = self.clean_filename(base_name)
        if base not in self.file_names:
            self.file_names[base] = 1
            return base + ".html"
        else:
            self.file_names[base] += 1
            return f"{base} {self.file_names[base]:02}.html"

    def parse(self, response):
        current_url = response.url
        if current_url in self.visited_urls:
            return
        self.visited_urls.add(current_url)

        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)

        try:
            language = detect(text_content)
        except:
            language = "unknown"

        page_title = soup.title.string if soup.title else urlparse(current_url).path.split("/")[-1] or "index"
        file_name = self.unique_filename(page_title)
        lang_dir = os.path.join("output", "html_pages", language)
        os.makedirs(lang_dir, exist_ok=True)
        full_path = os.path.join(lang_dir, file_name)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        for href in response.css("a::attr(href)").getall():
            full_url = urljoin(current_url, href)
            if urlparse(full_url).netloc == self.base_domain and full_url not in self.visited_urls:
                yield scrapy.Request(full_url, callback=self.parse)
