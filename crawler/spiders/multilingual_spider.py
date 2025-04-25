import scrapy
from bs4 import BeautifulSoup
from langdetect import detect
from urllib.parse import urlparse, urljoin
import os

class MultilingualSpider(scrapy.Spider):
    name = "multilingual_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("start_url is required to start crawling.")
        self.start_urls = [start_url]
        self.visited_urls = set()

    def parse(self, response):
        current_url = response.url
        if current_url in self.visited_urls:
            return
        self.visited_urls.add(current_url)

        # Extract page content
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)

        try:
            detected_lang = detect(text_content)
        except:
            detected_lang = "unknown"

        lang_dir = os.path.join("data", "raw", detected_lang)
        os.makedirs(lang_dir, exist_ok=True)

        # Save HTML page with a filename based on URL
        parsed_url = urlparse(current_url)
        filename = parsed_url.path.strip("/").replace("/", "_") or "index"
        file_path = os.path.join(lang_dir, f"{filename}.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Recursively follow internal links
        for href in response.css("a::attr(href)").getall():
            full_url = urljoin(response.url, href)
            if urlparse(full_url).netloc == urlparse(self.start_urls[0]).netloc:
                yield scrapy.Request(full_url, callback=self.parse)
