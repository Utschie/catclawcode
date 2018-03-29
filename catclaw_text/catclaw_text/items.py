# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatclawTextItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    league = scrapy.Field()
    cid = scrapy.Field()
    zhudui = scrapy.Field()
    kedui = scrapy.Field()
    companyname = scrapy.Field()
    timestamp = scrapy.Field()
    resttime = scrapy.Field()
    peilv = scrapy.Field()
    gailv = scrapy.Field()
    kailizhishu = scrapy.Field()
    fanhuanlv = scrapy.Field()
    pass
