# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DarazScrapyItem(scrapy.Item):
    title = scrapy.Field()
    # price = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()


class DarazItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()


class QuoteItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()
