# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from job_scraper.settings import MONGODB_DB, MONGODB_PORT, MONGODB_SERVER, MONGODB_COLLECTION
from scrapy.exceptions import DropItem
# from w3lib.html import remove_tags
from bs4 import BeautifulSoup

#MongoDBPipeline
class MongoDBPipeline:

   def __init__(self):
       connection = MongoClient(
           MONGODB_SERVER,
           MONGODB_PORT
       )
       db = connection[MONGODB_DB]
       self.collection = db[MONGODB_COLLECTION]

   def process_item(self, item, spider):
       self.collection.insert_one(dict(item))
       return item    

class CleanItemPipeline:
   def process_item(self, item, spider):
       item['details'] = BeautifulSoup(item['details']).get_text()
       return item

class CheckItemPipeline:
    def process_item(self, item, spider):
        if not item['title'] or not item['details']:
            raise DropItem("Missing field!")
        return item