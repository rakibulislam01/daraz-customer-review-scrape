# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DarazScrapyItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    reviewer_rating = scrapy.Field()
    review = scrapy.Field()
    date = scrapy.Field()
    sub_category = scrapy.Field()
    category = scrapy.Field()


class DarazItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    reviewer_rating = scrapy.Field()
    review = scrapy.Field()
    date = scrapy.Field()
    sub_category = scrapy.Field()
    category = scrapy.Field()


class QuoteItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()


class ReviewItem(scrapy.Item):
    title = scrapy.Field()
    total_rating = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    rating = scrapy.Field()
    current_date = scrapy.Field()
    reviewer_name = scrapy.Field()


