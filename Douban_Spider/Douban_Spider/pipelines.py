# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from bson.objectid import ObjectId


class DoubanSpiderPipeline(object):

    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017/")
        self.db = self.client['douban']

    def open_spider(self, item):
        print('爬虫开始了')

    def process_item(self, item, spider):
        """ 保存 """
        self.db.Doubancomment.insert_one(dict(item))
        print(item)
        print(type(item))
        print('=' * 40)
        return item

    def close_spider(self, item):
        print('爬虫结束了')
