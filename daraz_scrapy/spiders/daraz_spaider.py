import scrapy
import urllib
from scrapy_splash import SplashRequest
from ..items import DarazItem


daraz_link = [
    'https://www.daraz.com.bd/smartphones/xiaomi/?spm=a2a0e.searchlistcategory.cate_1_1.1.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/samsung/?spm=a2a0e.searchlistcategory.cate_1_1.2.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/nokia/?spm=a2a0e.searchlistcategory.cate_1_1.3.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/infinix/?spm=a2a0e.searchlistcategory.cate_1_1.4.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/alcatel1/?spm=a2a0e.searchlistcategory.cate_1_1.5.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/huawei/?spm=a2a0e.searchlistcategory.cate_1_1.6.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/motorola/?spm=a2a0e.searchlistcategory.cate_1_1.7.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/realme-201624/?spm=a2a0e.searchlistcategory.cate_1_1.8.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/vivo/?spm=a2a0e.searchlistcategory.cate_1_1.9.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/oppo/?spm=a2a0e.searchlistcategory.cate_1_1.10.5d28724epWQO7r',
    'https://www.daraz.com.bd/smartphones/umidigi/?spm=a2a0e.searchlistcategory.cate_1_1.11.5d28724epWQO7r'
]


class MySpider(scrapy.Spider):
    name = "daraz"
    start_urls = daraz_link

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 10})

    def parse(self, response):
        response_link = []
        for q in response.css(".c2prKC"):
            response_link_format = q.css(".cRjKsc a::attr(href)").extract_first()
            response_link_format = 'https:'+response_link_format
            response_link.append(response_link_format)
        for link in response_link:
            yield SplashRequest(url=link, callback=self.daz_scrap, args={'wait': 10})

    def daz_scrap(self, response):
        product = DarazItem()
        product["title"] = response.css('.pdp-mod-product-badge-title::text').extract()
        product["rating"] = response.css('.score-average::text').extract()
        product["review"] = response.css('.content::text').extract()
        yield product

