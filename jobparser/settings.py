BOT_NAME = 'jobparser'

SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

COOKIES_ENABLED = True

ITEM_PIPELINES = {
   'jobparser.pipelines.JobparserPipeline': 300,
}
