import scrapy
from scrapy_splash import SplashRequest
from ..items import DarazScrapyItem

link = [
    'https://www.daraz.com.bd/products/redmi-note-8-pro-653inches-6gb-ram-64gb-rom-20mp-selfie-camera-i122940818-s1043041557.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-note-7-pro-63inches-6gb-ram-64gb-rom-48mp-5mp-ai-dual-rear-camera-i114800431-s1032606336.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-mi-a3-6088inches-4gb-ram-64gb-rom-air-triple-camera-48mp-primary-camera-32mp-air-selfie-camera-i116510956-s1035490180.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-mi-a3-6088inches-4gb-ram-128gb-rom-i116506908-s1035540012.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-note-7s-63inches-4gb-ram-64gb-rom-48mp-5mp-ai-dual-rear-camera-i114792794-s1032624014.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-7-626-3gb-ram-32gb-rom-12mp-2mp-rear-dual-camera-i104212743-s1018970157.html?search=1',
    'https://www.daraz.com.bd/products/redmi-y3-smartphone-626-4gb-ram-64gb-rom-32mp-selfie-camera-i106362525-s1021352562.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-k20-pro-i112038261-s1028918970.html?search=1',
    'https://www.daraz.com.bd/products/mi-8-lite-24mp-selfie-camera-4gb-ram-64gb-rom-aurora-blue-i104096203-s1018810821.html?search=1',
    'https://www.daraz.com.bd/products/redmi-8-622inches-4gb-ram-64gb-rom-8mp-front-camera-i122937846-s1043040107.html?search=1',
    'https://www.daraz.com.bd/products/redmi-8-622inches-3gb-ram-32gb-rom-8mp-front-camera-i123033475-s1043136810.html?search=1',
    'https://www.daraz.com.bd/products/redmi-note-8-pro-653inches-6gb-ram-128gb-rom-20mp-selfie-camera-i123161377-s1043264451.html?search=1',
    'https://www.daraz.com.bd/products/redmi-note-6-pro-quad-camera-all-rounder-464gb-black-i101003043-s1014998025.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-7a-545-2gb-ram-32gb-rom-12mp-ai-rear-camera-i114802685-s1032618488.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-mi-cc9-pro-i127944935-s1047884330.html?search=1',
    'https://www.daraz.com.bd/products/xiaomi-redmi-note-8t-i127940778-s1047880388.html?search=1']


class MySpider(scrapy.Spider):
    name = "daraz_link"
    start_urls = link

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 10})

    def parse(self, response):
        quote = DarazScrapyItem()
        quote["title"] = response.css('.pdp-mod-product-badge-title::text').extract()
        quote["rating"] = response.css('.score-average::text').extract()
        quote["review"] = response.css('.content::text').extract()
        yield quote
        #
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     # follow element automatically go to the next page or execute the parse method.
        #     yield response.follow(next_page, callback=self.start_scraping)

        #
        # product_item_count = 1
        # next_product_link = response_link[product_item_count]
        # print('next_product_link===========================', next_product_link)
        # next_page = next_product_link
        # if next_page is not None:
        #     # follow element automatically go to the next page or execute the parse method.
        #     yield response.follow(next_page, callback=self.daz_scrap)
        #
