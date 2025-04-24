import scrapy
from urllib.parse import urljoin, urlparse
import os
from bs4 import BeautifulSoup
from langdetect import detect

class MultilingualSpider(scrapy.Spider):
    name = "multilingual_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(MultilingualSpider, self).__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("يرجى تحديد start_url")
        self.start_urls = [start_url]
        self.visited_urls = set()

    def parse(self, response):
        url = response.url
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        # استخراج النص لتحديد اللغة
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        try:
            lang = detect(text)
        except:
            lang = 'unknown'

        # إنشاء مجلد للغة إذا لم يكن موجودًا
        dir_path = os.path.join('data', 'raw', lang)
        os.makedirs(dir_path, exist_ok=True)

        # حفظ الصفحة
        parsed_url = urlparse(url)
        filename = parsed_url.path.strip('/').replace('/', '_') or 'index'
        filepath = os.path.join(dir_path, f"{filename}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)

        # متابعة الروابط الداخلية
        for href in response.css('a::attr(href)').getall():
            next_url = urljoin(response.url, href)
            if urlparse(next_url).netloc == urlparse(self.start_urls[0]).netloc:
                yield scrapy.Request(next_url, callback=self.parse)
