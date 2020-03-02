import datetime
import urllib
import requests
import scrapy
from scrapy_splash import SplashRequest

from ..items import ReviewItem

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

mobile_link = [
    'https://www.daraz.com.bd/smartphones/xiaomi/?spm=a2a0e.searchlistcategory.cate_1_1.1.5d28724epWQO7r'
]


class MySpider(scrapy.Spider):
    name = "daraz"
    start_urls = daraz_link
    page_number = 2

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
            yield SplashRequest(url=link, callback=self.daz_scrap, args={'wait': 20})

    def daz_scrap(self, response):
        product_id = response
        product_item_id = product_id.url.split('-')[-2][1:]
        product = ReviewItem()
        total_review = response.css('.item')
        time_ = datetime.datetime.now().date()
        time_ = time_.strftime('%Y/%m/%d')
        product["title"] = response.css('.pdp-mod-product-badge-title::text').extract()
        product["total_rating"] = response.css('.score-average::text').extract()
        # product_item = response.css('.key-li:nth-child(2) .key-value::text').extract()
        # product_item_id = product_item[0].split('_')[0]

        for item in total_review:
            rating = item.css('.starCtn .star::attr(src)').extract()
            rating_value = 0
            for i in rating:
                j = i.split('/')
                if j[4] == 'TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png':
                    rating_value += 1
            product["content"] = item.css('.content::text').extract() or None
            product["rating"] = rating_value
            product["date"] = item.css('.title.right::text').extract()
            product["reviewer_name"] = item.css('.middle span:nth-child(1)::text').extract()
            product["current_date"] = time_
            yield product
        MySpider.page_number = 2
        next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId='+product_item_id+'&pageSize=5&filter=0&sort=0&pageNo='+str(MySpider.page_number)
        yield response.follow(next_page, callback=self.ajax_page, meta={'product_item_id': product_item_id})

    def ajax_page(self, response):
        product_item_id = response.meta.get('product_item_id')
        time_ = datetime.datetime.now().date()
        time_ = time_.strftime('%Y/%m/%d')
        product = ReviewItem()
        link_url = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId='+str(product_item_id)+'&pageSize=5&filter=0&sort=0&pageNo='+str(MySpider.page_number)
        url = requests.get(link_url)
        json_value = url.json()
        js = json_value['model']['items']
        item_id = json_value['model']['item']['itemId']
        avg_rating = json_value['model']['ratings']
        paging = json_value['model']['paging']['totalPages']
        for i in js:
            product['reviewer_name'] = i['buyerName']
            product["content"] = i['reviewContent']
            product["rating"] = i['rating']
            product["date"] = i['reviewTime']
            product["title"] = i['itemTitle']
            product["total_rating"] = avg_rating['average']
            product["current_date"] = time_
            yield product

        if MySpider.page_number < paging:
            MySpider.page_number += 1
            next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId='+str(item_id)+'&pageSize=5&filter=0&sort=0&pageNo='+str(MySpider.page_number)
            yield response.follow(next_page, callback=self.ajax_page, meta={'product_item_id': product_item_id})


