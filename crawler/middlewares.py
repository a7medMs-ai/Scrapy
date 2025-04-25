from scrapy import signals

class CustomMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")
