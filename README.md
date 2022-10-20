# Open Source Proxy Benchmarking Tool
Open source proxy benchmarking tool that anyone can run to get accurate, transparent performance results. 
It is a [Scrapy](https://scrapy.org/) spider that crawls [Similarweb Top 50 websites](https://www.similarweb.com/top-websites/) with 
up to 1,000 URLs per website (maximum 50,000 URLs) and reports the results per proxy provider. 

Alternatively, you can also supply a custom CSV with your own URLs to the spider. 

If you choose to run the spider this way, the spider will only follow the URLs in the CSV, and will not follow any links inside them (unlike the default method).

## QuickStart

1. **Install [Scrapy](https://scrapy.org/) and [scrapy-zyte-api](https://github.com/scrapy-plugins/scrapy-zyte-api#readme)**

```
python3 -m pip install --upgrade pip
python3 -m pip install scrapy
python3 -m pip install scrapy-zyte-api
```

2. **Configure the `proxybench/settings.py` file with the credentials you have and comment out the rest**

```
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
```

3. **Run**

```
scrapy crawl proxybench
```
This will run the spider normally and crawl [Similarweb Top 50 websites](https://www.similarweb.com/top-websites/).

However, if you wish to crawl a custom list of URLs, you can use the links_csv argument as such:
```
scrapy crawl proxybench -a links_csv=C:/foo/bar/links.csv
```
The links CSV needs to have a column named "Links". 

4. **Check the results in the `log.txt` file**

```
 'proxybench/brightdata_web_unlocker/successful': 33753,
 'proxybench/brightdata_web_unlocker/total': 38357,
 'proxybench/oxylabs_web_scraper_api/successful': 32471,
 'proxybench/oxylabs_web_scraper_api/total': 38234,
 'proxybench/zyte_smart_browser/successful': 38397,
 'proxybench/zyte_smart_browser/total': 40462,
 'proxybench/zyte_smart_proxy_manager/successful': 36841,
 'proxybench/zyte_smart_proxy_manager/total': 40239,
```
