BOT_NAME = "localization_tool"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "crawler.pipelines.LocalizationPipeline": 300,
}

FEEDS = {
    "data/output.jsonl": {
        "format": "jsonlines",
        "encoding": "utf8",
        "store_empty": False,
    }
}


DEPTH_LIMIT = 2  # prevent crawling too deep
LOG_LEVEL = "INFO"
