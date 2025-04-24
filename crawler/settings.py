BOT_NAME = 'localization_tool'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'crawler.pipelines.LocalizationPipeline': 300,
}
