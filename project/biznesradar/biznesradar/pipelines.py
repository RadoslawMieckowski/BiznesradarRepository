# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import sqlite3
import pymongo

class BiznesradarPipeline(object):

    def __init__(self):
        # self.create_connection()
        # self.create_table()
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['biznesradar_spider']
        self.collection = db['biznesradar_tb']
    
    # Don't need the following code, for there's Mongodb instead :)
    # def create_connection(self):
    #     self.conn= sqlite3.connect('biznesradar.db')
    #     self.curr= self.conn.cursor()
    #
    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS indicators_tb""")
    #     self.curr.execute("""CREATE TABLE indicators_tb(
    #                 date TEXT, nameOfCompany TEXT, isToBuy TEXT,
    #                 price REAL, priceToBV REAL, priceToSalesPerShare REAL,
    #                 priceToProfit REAL, priceToOperationalProfit REAL,
    #                 ROE REAL, ROA REAL
    #                 )""")

    def process_item(self, item, spider):
        # self.store_db(item)
        self.collection.insert(dict(item))
        return item

    # def store_db(self,item):
    #     self.conn.commit()  
    #     self.curr.execute("""INSERT INTO indicators_tb VALUES(?,?,?,?,?,?,?,?,?,?)""",(
    #                         item['date'][0],
    #                         item['nameOfCompany'][0],
    #                         item['isToBuy'][0],
    #                         item['price'][0],
    #                         item['priceToBV'][0:4],
    #                         item['priceToSalesPerShare'][0:4],
    #                         item['priceToProfit'][0:4],
    #                         item['priceToOperationalProfit'][0:4],
    #                         item['ROE'][0:4],
    #                         item['ROA'][0:4]
    #     ))
