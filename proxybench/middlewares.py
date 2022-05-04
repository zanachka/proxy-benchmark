import logging
from scrapy.exceptions import IgnoreRequest

BAN_BODY_FINGERPRINTS = [
    'There was a problem with this request',
    'Rate limit exceeded',
    '<div id="captcha',
    'computer or network may be sending automated queries',
    'que no eres un robot',
    'Our systems have detected unusual traffic from your computer network',
    'recaptcha_challenge_field',
    '<div class="g-recaptcha"',
    '/error/500_503',
    'Enter the characters you see below',
    'validateCaptcha',
    'opfcaptcha',
    'To discuss automated access',
    '{"statusCode":10000,"verifyConfig":{"code":10000',
    '<div class="verify-wrap"',
]

BAN_REDIRECT_URL_FINGERPRINTS = [
    '/login',
    '?continue=',
    '/showcaptcha',
]


class BanError(IgnoreRequest):
    pass


class BanDetectionMiddleware:
    def is_ban(self, response):
        body = response.text if hasattr(response, 'text') else None
        url = response.url
        provider = response.meta['provider']
        content_length = response.headers.get('content-length')

        if body == '':
            logging.debug(f'Ban (empty body) {provider}: {url}')
            return True

        if content_length in [0, 277]:
            logging.debug(f'Ban (content-length = 0 or 277) {provider}: {url}')
            return True

        for fp in BAN_REDIRECT_URL_FINGERPRINTS:
            if 'redirect_urls' in response.meta and fp in url:
                logging.debug(f'Ban (redirect to "{fp}") {provider}: {url}')
                return True

        for fp in BAN_BODY_FINGERPRINTS:
            if body and fp in body:
                logging.debug(f'Ban (body with "{fp}") {provider}: {url}')
                return True

        return False

    def process_spider_input(self, response, spider):
        if self.is_ban(response):
            raise BanError

        return

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, BanError):
            return []
