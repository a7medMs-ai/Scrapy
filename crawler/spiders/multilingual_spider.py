import scrapy
from bs4 import BeautifulSoup
from langdetect import detect
from urllib.parse import urlparse, urljoin
from crawler.items import PageItem

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

        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)

        try:
            detected_lang = detect(text_content)
        except:
            detected_lang = "unknown"

        # ✅ Create and yield a Scrapy item
        item = PageItem()
        item["url"] = current_url
        item["language"] = detected_lang
        item["content"] = text_content[:1000]  # limit to avoid huge files
        item["html"] = response.text[:2000]    # limit for performance

        yield item

        # ✅ Continue crawling internal links
        for href in response.css("a::attr(href)").getall():
            full_url = urljoin(response.url, href)
            if urlparse(full_url).netloc == urlparse(self.start_urls[0]).netloc:
                yield scrapy.Request(full_url, callback=self.parse)
