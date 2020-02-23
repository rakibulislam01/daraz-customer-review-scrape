import scrapy
from scrapy_splash import SplashRequest
from ..items import DarazScrapyItem

link = ['https://www.daraz.com.bd/products/huawei-y6s-smartphone-609inches-3gb-ram-64gb-rom-13mp-i126979834-s1047017443.html?spm=a2a0e.searchlist.list.1.32af1781bXJ9eV&search=1']


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
        quote["review"] = response.css('.content::text').extract() or None
        quote["reviewer_rating"] = response.css('.starCtn .star::attr(src)').extract()
        quote["date"] = response.css('.title.right::text').extract()
        quote["sub_category"] = response.css('.breadcrumb_item+ .breadcrumb_item .breadcrumb_item_anchor span::text').extract()
        quote["category"] = response.css('.breadcrumb_item:nth-child(1) a::attr(title)').extract()
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
