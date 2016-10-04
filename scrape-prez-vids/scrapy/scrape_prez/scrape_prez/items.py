# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class prezItem(scrapy.Item):
    weekly_address_url = scrapy.Field()
    speechText = scrapy.Field()
    rawText = scrapy.Field()
    videoLink = scrapy.Field()
    video = scrapy.Field()
    file_urls = scrapy.Field()
    speechTitle = scrapy.Field()


class AKCItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    breed = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    thumb = scrapy.Field()

class WikiItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    breed = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
