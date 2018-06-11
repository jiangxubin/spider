# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    #文本名字
    author = scrapy.Field()
    #作者名字
    novelurl = scrapy.Field()
    #地址
    serialnumber = scrapy.Field()
    #字数
    category = scrapy.Field()
    #类别
    name_id = scrapy.Field()
    #小说编号
    pass
