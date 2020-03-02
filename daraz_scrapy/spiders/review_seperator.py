import scrapy
from scrapy_splash import SplashRequest
from ..items import ReviewItem
import datetime
import requests

link = [
    # 'https://www.daraz.com.bd/products/xiaomi-redmi-7-626-3gb-ram-32gb-rom-12mp-2mp-rear-dual-camera-i104212743-s1018970157.html?spm=a2a0e.searchlistcategory.list.12.6b9d55b4WEtJct&search=1'
    # 'https://www.daraz.com.bd/products/uiisii-c100-in-ear-earphone-with-mic-black-i120278445-s1039712541.html?spm=a2a0e.11884278.1001.djfy_6.194b43a6Rpk7hC&scm=1007.19098.120041.0&pvid=063e6b3c-9bf7-45b1-86cb-4d9e9c925693'
    # 'https://www.daraz.com.bd/products/dm10-in-ear-earphone-black-i2528297-s123298926.html?spm=a2a0e.searchlistcategory.list.1.61742d58eKYpdx&search=1'
    # 'https://www.daraz.com.bd/products/dm7-zinc-alloy-hifi-super-bass-in-ear-earphones-black-i2539082-s126398182.html?spm=a2a0e.searchlistcategory.list.4.768f2d58ZoMPmT&search=1'
    # 'https://www.daraz.com.bd/products/uiisii-hm12-gaming-headset-on-ear-deep-bass-good-treble-earphone-black-i105116842-s1019960858.html?spm=a2a0e.searchlistcategory.list.6.768f2d58ZoMPmT&search=1'
    # 'https://www.daraz.com.bd/products/mi-in-ear-headphone-basic-black-i275435-s1245309.html?spm=a2a0e.searchlistcategory.list.18.768f2d58ZoMPmT&search=1'
    # 'https://www.daraz.com.bd/products/mini-drink-frother-multicolor-i802565-s3397366.html?spm=a2a0e.searchlistcategory.list.10.456725a9JrAfjC&search=1'
    # 'https://www.daraz.com.bd/products/led-strip-light-with-remote-15-feet-rgb-colour-i111432110-s1028382060.html?spm=a2a0e.searchlistcategory.list.6.66203b0euZtkwc&search=1'
    # 'https://www.daraz.com.bd/products/fairy-decorative-lights-yellow-i214007-s1079910.html?spm=a2a0e.searchlistcategory.list.10.66203b0euZtkwc&search=1'
    # 'https://www.daraz.com.bd/products/31-in-1-screw-driver-set-yellow-and-red-i842605-s3501152.html?spm=a2a0e.searchlistcategory.list.16.7ec2355bIO796w&search=1'
    # 'https://www.daraz.com.bd/products/multiplug-extension10-port-socket-hp-0555-i105626265-s1020496756.html?spm=a2a0e.searchlistcategory.bestshown_1.8.489055b3shEVoT&search=1'
    # 'https://www.daraz.com.bd/products/vikan-android-smart-hd-led-tv-32-black-i888111-s3666215.html?spm=a2a0e.searchlistcategory.list.2.4de328e1o4spy1&search=1'
    'https://www.daraz.com.bd/products/gerber-baby-towels-set-8-pieces-i50037-s410244.html?spm=a2a0e.searchlistcategory.list.72.7444a596Kov5N7&search=1'
]

# Ajax_url = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=114792794&pageSize=5&filter=0&sort=0&pageNo=3'


class MySpider(scrapy.Spider):
    name = "customer_review"
    page_number = 1
    start_urls = link

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 10})

    def parse(self, response):
        product_id = response
        product_item_id = product_id.url.split('-')[-2][1:]
        # product_item_id = '50037'
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

        next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId=' + product_item_id + '&pageSize=20&filter=0&sort=0&pageNo='+str(MySpider.page_number)
        yield response.follow(next_page, callback=self.ajax_page,  meta={'product_item_id': product_item_id})

    def ajax_page(self, response):
        product_item_id = response.meta.get('product_item_id')
        # product_item_id = '50037'
        time_ = datetime.datetime.now().date()
        time_ = time_.strftime('%Y/%m/%d')
        product = ReviewItem()
        link_url = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId='+str(product_item_id)+'&pageSize=20&filter=0&sort=0&pageNo='+str(MySpider.page_number)
        url = requests.get(link_url)
        json_value = url.json()
        js = json_value['model']['items']
        item_id = json_value['model']['item']['itemId']
        # item_id = '50037'
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
            next_page = 'https://my.daraz.com.bd/pdp/review/getReviewList?itemId='+str(item_id)+'&pageSize=20&filter=0&sort=0&pageNo='+str(MySpider.page_number)
            yield response.follow(next_page, callback=self.ajax_page, meta={'product_item_id': product_item_id})

