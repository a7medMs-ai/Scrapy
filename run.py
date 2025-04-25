import sys
import os
os.makedirs("data", exist_ok=True)
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.multilingual_spider import MultilingualSpider
from utils.word_counter import analyze_html_files
from utils.zip_creator import create_language_zips

def run_crawler(start_url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(MultilingualSpider, start_url=start_url)
    process.start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run.py <start_url>")
        sys.exit(1)
    start_url = sys.argv[1]
    run_crawler(start_url)
    analyze_html_files('data/raw', start_url)
    create_language_zips('data/raw')
