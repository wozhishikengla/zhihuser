# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#定义数据，获取数据名称
class ZhihuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    headline = scrapy.Field()
    domicile = scrapy.Field()
    career= scrapy.Field()
    educational_experice = scrapy.Field()
    individual_resume= scrapy.Field()
    

