# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    """
    define the fields for your item here
    """
    url = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    processed = scrapy.Field()
