import scrapy

from ..items import BiznesradarItem


class BiznesradarSpiderSpider(scrapy.Spider):
    name = 'biznesradar_spider'
    # allowed_domains = ['https://www.biznesradar.pl/gielda/indeks:WIG20']
    start_urls = ['https://www.biznesradar.pl/gielda/indeks:WIG20']
    #'https://www.biznesradar.pl/notowania/ASSECO-POLAND#1d_lin_lin'
  
    # https://docs.scrapy.org/en/latest/intro/tutorial.html#response-follow-example

    def parse(self,response):

        site = 'https://www.biznesradar.pl'
        temp_list = response.css('.wname::attr(href)').extract()

        links=[]
        for x in range(len(temp_list)):
            links.append(site + temp_list[x])
        print(links)

        counter=0
        for link in links: #response.url:
            counter+=1
            print(counter)
            yield response.follow(link, callback=self.createItem)

    def createItem(self, response):
        items = BiznesradarItem()
     
        container = response.css('#profile-header')
        nameOfCompany = container.css('h2::text').extract()
        price = container.css('.q_ch_act::text').extract()
        date = container.css('.q_ch_date::text').extract()
        isToBuy = response.css('.indicator-result::text').extract()

        table_of_indicators = response.css('.ratios')
        priceToBV = table_of_indicators.css('.ratios .name+ .value span::text')[0].extract()
        priceToSalesPerShare = table_of_indicators.css('.ratios .name+ .value span::text')[1].extract()

        items['nameOfCompany'] = nameOfCompany
        items['price'] = price
        items['date'] = date
        items['isToBuy'] = isToBuy
        items['priceToBV'] = priceToBV
        items['priceToSalesPerShare'] = priceToSalesPerShare


        try:
            ROE = table_of_indicators.css('.ratios .name+ .value span::text')[4].extract()
        except IndexError:
            ROE = None

        try:
            ROA = table_of_indicators.css('.ratios .name+ .value span::text')[5].extract()
        except:
            ROA = None

        try:
            priceToProfit = table_of_indicators.css('.ratios .name+ .value span::text')[2].extract()
        except:
            priceToProfit = None

        try:
            priceToOperationalProfit = table_of_indicators.css('.ratios .name+ .value span::text')[3].extract()
        except:
            priceToOperationalProfit = None

     

        items['priceToProfit'] = priceToProfit
        items['priceToOperationalProfit'] = priceToOperationalProfit
        items['ROE'] = ROE
        items['ROA'] = ROA

        yield items
