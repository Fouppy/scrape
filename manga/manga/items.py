# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    release_date = scrapy.Field()
    collection = scrapy.Field()
    cover = scrapy.Field()
    tome = scrapy.Field()
    # pass
