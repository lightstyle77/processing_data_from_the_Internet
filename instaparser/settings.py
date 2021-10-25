IMAGES_STORE = 'images'

BOT_NAME = 'instaparser'

SPIDER_MODULES = ['instaparser.spiders']
NEWSPIDER_MODULE = 'instaparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.693 Yowser/2.5 Safari/537.36'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 8

DOWNLOAD_DELAY = 1.5
COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'instaparser.pipelines.InstagramPipeline': 300,
    'instaparser.pipelines.InstagramlinImgPipeline': 100
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True
