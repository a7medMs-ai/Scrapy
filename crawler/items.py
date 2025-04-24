import scrapy

class PageItem(scrapy.Item):
    url = scrapy.Field()
    language = scrapy.Field()
    content = scrapy.Field()
