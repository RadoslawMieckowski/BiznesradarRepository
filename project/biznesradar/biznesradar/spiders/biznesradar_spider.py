import scrapy

from ..items import BiznesradarItem
# import requests
# proxy=''
# r=requests.get('https://httpbin.org/ip',proxies={'http':proxy,'https':proxy},timeout=3)
# print(r.json())

class BiznesradarSpiderSpider(scrapy.Spider):
    name = 'biznesradar_spider'
    # allowed_domains = ['https://www.biznesradar.pl/gielda/indeks:WIG20']
    start_urls = ['https://www.biznesradar.pl/gielda/indeks:WIG20']
    #'https://www.biznesradar.pl/notowania/ASSECO-POLAND#1d_lin_lin'
    #trzeba by zacząć od    https://www.biznesradar.pl/gielda/indeks:WIG20
    # ponieważ to wig 20 więc pętla  for i in range(20)....
    # https://docs.scrapy.org/en/latest/intro/tutorial.html#response-follow-example

    def parse(self,response):

        co_skrapujemy = 'https://www.biznesradar.pl'
        temp_list = response.css('.wname::attr(href)').extract()
        # print(co_skrapujemy)
        # print(temp_list)
        # print(temp_list[19])
        # print(response.url)  #wazne
        links=[]
        for x in range(len(temp_list)):
            links.append(co_skrapujemy + temp_list[x])
        print(links)

        counter=0
        for link in links: #response.url:
            counter+=1
            print(counter)
            yield response.follow(link, callback=self.createItem)

    def createItem(self, response):
        items = BiznesradarItem()
        # list = response.css('td.selectorgadget_selected a::attr(href)')
        # for company in range(20):
        #     link = list[company]
        #     print(response.url)
        #     yield response.follow(link, callback=self.parse)


        ogolne = response.css('#profile-header')
        nameOfCompany = ogolne.css('h2::text').extract()
        price = ogolne.css('.q_ch_act::text').extract()
        date = ogolne.css('.q_ch_date::text').extract()
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

        # rows = table_of_indicators.css('tr::text').extract_all()


            # for x in table_of_indicators:
            #     print(table_of_indicators.css('tr::text')

        items['priceToProfit'] = priceToProfit
        items['priceToOperationalProfit'] = priceToOperationalProfit
        items['ROE'] = ROE
        items['ROA'] = ROA

            # items['rows']=rows
        yield items