# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class DomainsPipeline(object):

    def __init__(self,mongo_uri='',mongo_db='domains', default_collection='domains'):
        self.client = pymongo.MongoClient(host=mongo_uri,retryWrites=False)
        self.db = self.client[mongo_db]
        self.col = self.db[default_collection]

    def process_item(self,item,spider):
        self.col.save(item)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'domains'),
            default_collection = crawler.settings.get('DEFAULT_COLLECTIONS', 'domains')
        )

    def close_spider(self,spider):
        self.client.close()
