import scrapy
import tldextract


def patch_request(request, provider, proxy):
    if provider == 'zyte_smart_browser':
        request.meta['provider'] = provider
        request.meta['zyte_api'] = {'browserHtml': True}
    else:
        request.meta['provider'] = provider
        request.meta['proxy_str'] = proxy
        request.meta['proxy'] = proxy


def get_original_domain(request):
    if 'redirect_urls' in request.meta:
        url_original = request.meta['redirect_urls'][0]
    else:
        url_original = request.url

    return tldextract.extract(url_original).registered_domain.lower()


class ProxyBenchmarkSpider(scrapy.Spider):
    name = 'proxybench'
    start_url = 'https://www.similarweb.com/top-websites/'
    link_extractor = scrapy.linkextractors.LinkExtractor(allow_domains=[])
    _latency_total = {}

    def start_requests(self):
        for provider, proxy in self.settings['PROXY_PROVIDERS'].items():
            request = scrapy.Request(self.start_url, self.parse_start_url)
            patch_request(request, provider, proxy)
            yield request

    def parse_start_url(self, response):
        provider = response.meta['provider']
        proxy = response.meta.get('proxy_str')

        for request in response.follow_all(css='a.topRankingGrid-blankLink'):
            domain = tldextract.extract(request.url).registered_domain.lower()
            self.link_extractor.allow_domains.add(domain)

            self.increment_counters(provider, domain, 'total')
            patch_request(request, provider, proxy)
            yield request

    def parse(self, response):
        provider = response.meta['provider']
        proxy = response.meta.get('proxy_str')
        domain_original = get_original_domain(response.request)
        self.increment_counters(provider, domain_original, 'successful')
        latency = response.meta.get('download_latency')
        self.increment_latency(provider, domain_original, latency)

        for link in self.link_extractor.extract_links(response):
            domain = tldextract.extract(link.url).registered_domain.lower()
            total = self.get_counter(provider, domain, 'total')

            if total < self.settings['REQUESTS_PER_DOMAIN']:
                request = scrapy.Request(link.url)

                self.increment_counters(provider, domain, 'total')
                patch_request(request, provider, proxy)
                yield request

    def increment_counters(self, provider, domain, counter):
        stats = self.crawler.stats
        stats.inc_value(f'proxybench/{provider}/{counter}', 1)
        stats.inc_value(f'proxybench/{provider}/{domain}/{counter}', 1)

    def get_counter(self, provider, domain, counter):
        stats = self.crawler.stats
        return stats.get_value(f'proxybench/{provider}/{domain}/{counter}', 0)

    def increment_latency(self, provider, domain, value):
        d = self._latency_total
        d[f'proxybench/{provider}'] = d.setdefault(f'proxybench/{provider}', 0) + value
        d[f'proxybench/{provider}/{domain}'] = d.setdefault(f'proxybench/{provider}/{domain}', 0) + value

    def calculate_latency_avg(self):
        stats = self.crawler.stats
        for key, latency_total in self._latency_total.items():
            response_cnt = stats.get_value(f'{key}/successful', 1)
            stats.set_value(f'{key}/latency_avg', latency_total/response_cnt)

    def closed(self, reason):
        self.calculate_latency_avg()
