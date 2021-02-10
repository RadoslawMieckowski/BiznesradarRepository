# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiznesradarItem(scrapy.Item):
    # define the fields for your item here like:

    price = scrapy.Field()
    nameOfCompany = scrapy.Field()
    date = scrapy.Field()
    isToBuy = scrapy.Field()
    priceToBV=scrapy.Field()
    priceToSalesPerShare=scrapy.Field()
    priceToProfit=scrapy.Field()
    priceToOperationalProfit=scrapy.Field()
    ROE=scrapy.Field()
    ROA=scrapy.Field()
    rows=scrapy.Field()

