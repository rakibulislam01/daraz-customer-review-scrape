import scrapy
from scrapy_splash import SplashRequest
from ..items import ReviewItem
import datetime
import requests

link = [
    'https://www.daraz.com.bd/products/xiaomi-redmi-note-7-pro-63inches-6gb-ram-64gb-rom-48mp-5mp-ai-dual-rear-camera-i114800431-s1032606336.html?spm=a2a0e.searchlistcategory.list.3.34ef55b4ooI8sd&search=1']
dictonary = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
Ajax_url = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=114792794&pageSize=5&filter=0&sort=0&pageNo=3'


class MySpider(scrapy.Spider):
    name = "customer_review"
    page_number = 2
    start_urls = link

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 10})

    def parse(self, response):
        product = ReviewItem()
        total_review = response.css('.item')
        time_ = datetime.datetime.now().date()
        time_ = time_.strftime('%Y/%m/%d')
        product["title"] = response.css('.pdp-mod-product-badge-title::text').extract()
        product["total_rating"] = response.css('.score-average::text').extract()

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

        next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=114792794&pageSize=5&filter=0&sort=0&pageNo=' + str(MySpider.page_number)
        yield response.follow(next_page, callback=self.ajax_page)

    def ajax_page(self, response):
        time_ = datetime.datetime.now().date()
        time_ = time_.strftime('%Y/%m/%d')
        product = ReviewItem()
        # link_url = response
        link_url = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=114792794&pageSize=5&filter=0&sort=0&pageNo='+str(MySpider.page_number)
        url = requests.get(link_url)
        json_value = url.json()
        js = json_value['model']['items']
        avg_rating = json_value['model']['ratings']
        paging = json_value['model']['paging']['totalPages']
        for i in js:
            print('============================================', i)
            product['reviewer_name'] = i['buyerName']
            product["content"] = i['reviewContent']
            product["rating"] = i['rating']
            product["date"] = i['reviewTime']
            product["title"] = i['itemTitle']
            product["total_rating"] = avg_rating['average']
            product["current_date"] = time_

        if MySpider.page_number <= 5:
            MySpider.page_number += 1
            next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=114792794&pageSize=5&filter=0&sort=0&pageNo='+str(MySpider.page_number)
            yield response.follow(next_page, callback=self.ajax_page)


