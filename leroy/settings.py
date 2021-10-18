BOT_NAME = 'leroy'

SPIDER_MODULES = ['leroy.spiders']
NEWSPIDER_MODULE = 'leroy.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
IMAGES_STORE = 'img'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203'

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1.5

COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'leroy.pipelines.LeroyPipeline': 300,
    'leroy.pipelines.ImagesLoader': 200,
}
