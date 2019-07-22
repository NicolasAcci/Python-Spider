# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from openpyxl import Workbook
from city58_second_goods.items import *
from pymongo import MongoClient


class MongodbSecondGoodsPipeline(object):
    '''保存到mongodb'''
    def __init__(self,
                 databaseIp='127.0.0.1',
                 databasePort=27017,
                 # user="mongo",
                 # password=None, #没有设置用户和密码
                 mongodbName='second_goods'):
        client = MongoClient(databaseIp, databasePort)
        self.db = client[mongodbName]
        # self.db.authenticate(user, password)

    def process_item(self, item, spider):
        if isinstance(item, GoodsItem):
            postItem = dict(item)  # 把item转化成字典形式
            self.db.scrapy.insert(postItem)  # 向数据库插入一条记录
        return item


class MysqlSecondGoodsPipeline(object):
    '''保存到mysql'''

    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'second_goods',
            'charset': 'utf8'
        }
        #设置数据库的配置
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute("""
                insert into goods(goods_title,goods_time,goods_price,goods_color,goods_area,goods_cate) values(%s,%s,%s,%s,%s,%s)
                """, (
            item['goods_title'], item['goods_time'], item['goods_price'], item['goods_color'], item['goods_area'],
            item['goods_cate']))
        #sql语句插入数据
        self.conn.commit()
        return item


class XslxSecondGoodsPipeline(object):
    '''保存到xslx'''

    def open_spider(self, spider):
        self.wb = Workbook()
        # 创建excel
        self.ws = self.wb.active
        # 设置表头信息
        self.ws.append(['标题', '时间', '价格', '颜色', '地区', '备注'])

    def process_item(self, item, spider):
        line = [item['goods_title'], item['goods_time'], item['goods_price'], item['goods_color'], item['goods_area'],
                item['goods_cate']]
        # 注意列表的顺序
        self.ws.append(line)
        return item

    def close_spider(self, spider):
        self.wb.save('goods.xlsx')


class CsvSecondGoodsPipeline(object):
    '''保存到csv或json'''

    def process_item(self, item, spider):
        if isinstance(item, City58SecondGoodsItem):  # 用来判断是哪个item
            json_str = json.dumps(dict(item), ensure_ascii=False)
            with open("url.csv", "a", encoding="utf-8") as f:
                f.write(json_str + '\n')
        elif isinstance(item, GoodsItem):
            json_str = json.dumps(dict(item), ensure_ascii=False)
            with open("goods.csv", "a", encoding="utf-8") as f:
                f.write(json_str + '\n')
        return item
