PROXY_PROVIDERS = {
    # https://brightdata.com/products/web-unlocker
    'brightdata_web_unlocker': 'http://lum-customer-<id>-zone-unblocker:<password>@zproxy.lum-superproxy.io:22225',
    # https://oxylabs.io/products/scraper-api/web
    'oxylabs_web_scraper_api': 'http://<user>:<password>@realtime.oxylabs.io:60000',
    # https://www.zyte.com/smart-browser-api-anti-fingerprinting/
    'zyte_smart_browser': '<zyte_data_api_key>',
    # https://www.zyte.com/smart-proxy-manager/
    'zyte_smart_proxy_manager': 'http://<smart_proxy_manager_api_key>:@proxy.zyte.com:8011',
}
LOG_FILE = 'log.txt'
REQUESTS_PER_DOMAIN = 1000
CONCURRENT_REQUESTS = 50
ROBOTSTXT_OBEY = False
RETRY_ENABLED = False
COOKIES_ENABLED = False
BOT_NAME = 'proxybench'
SPIDER_MODULES = ['proxybench.spiders']
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
DUPEFILTER_CLASS = 'proxybench.dupefilter.ProviderwiseDupeFilter'
SPIDER_MIDDLEWARES = {'proxybench.middlewares.BanDetectionMiddleware': 950}
DOWNLOAD_HANDLERS = {
    'http': 'scrapy_zyte_api.handler.ScrapyZyteAPIDownloadHandler',
    'https': 'scrapy_zyte_api.handler.ScrapyZyteAPIDownloadHandler',
}
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
ZYTE_API_KEY = PROXY_PROVIDERS.get('zyte_smart_browser')
