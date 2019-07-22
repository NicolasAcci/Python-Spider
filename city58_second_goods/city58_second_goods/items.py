# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City58SecondGoodsItem(scrapy.Item):
    goods_url = scrapy.Field()
    #一级页面url


class GoodsItem(scrapy.Item):
    goods_title = scrapy.Field()
    #标题
    goods_time = scrapy.Field()
    #时间
    goods_price = scrapy.Field()
    #价格
    goods_color = scrapy.Field()
    #颜色
    goods_area = scrapy.Field()
    #地区
    goods_cate = scrapy.Field()
    #备注



