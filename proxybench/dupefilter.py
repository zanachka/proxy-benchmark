from scrapy.dupefilters import RFPDupeFilter
from proxybench.spiders.proxybench_spider import get_original_domain


def decrement_counters(spider, provider, domain, counter):
    stats = spider.crawler.stats
    stats.get_stats()[f'proxybench/{provider}/{counter}'] -= 1
    stats.get_stats()[f'proxybench/{provider}/{domain}/{counter}'] -= 1


class ProviderwiseDupeFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        provider = request.meta['provider']
        return super().request_fingerprint(request) + provider

    def log(self, request, spider):
        super().log(request, spider)

        provider = request.meta['provider']
        domain = get_original_domain(request)
        decrement_counters(spider, provider, domain, 'total')
