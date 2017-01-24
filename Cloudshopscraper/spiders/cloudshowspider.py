# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Cloudshopscraper.items import CloudshopscraperItem
import requests
import re

class CloudshowspiderSpider(scrapy.Spider):
    name = "cloudshowspider"
    allowed_domains = ["cloudshowplace.com"]
    start_urls = (
        'http://www.cloudshowplace.com/application/',
    )

    def parse(self, response):

        for i in range(1, 44):

            res_get = requests.get(  url='http://www.cloudshowplace.com/ODD_FILES/jcm/load_data.php?queryType=application&appid=%d&_=1485191630610' % i,
                                 headers={ 'X-Requested-With': 'XMLHttpRequest'} )
       
            company_list = res_get.text.split('$.fancybox.open')

            for company in company_list:

                try:

                    # href : 'http://www.cloudshowplace.com/ODD_FILES/jcm/get_company.php?key=2935',type
                    com_url = re.search( r'href : \'(.*?)\'\,.*type', company, re.M|re.I|re.S )
                    comp_url = com_url.group(1)

                    sub_url = re.search( r'jcm/(.*?).php', comp_url, re.M|re.I|re.S )
                    if ( sub_url.group(1) != "awardSummary"):
    
                        req = Request( url=comp_url, callback=self.company_detail, dont_filter=True )
                        yield req

                except:
                    pass

    def company_detail(self, response):

        # self.logger.info( "-----------------------------" )
        # self.logger.info( response )

        item = CloudshopscraperItem()

        data_trs = response.xpath('//div[@id="divMain"]/div[@id="divContent"]/table/tr')

        for data_tr in data_trs:

            data_level = ' '.join(data_tr.xpath('td/div[@class="divTitle"]/text()').extract()).strip()

            if( data_level == "Company Name:" ):
                item['Company_Name'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Address 1:" ):
                item['Address_1'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Address 2:" ):
                item['Address_2'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "City:" ):
                item['City'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "State/Province:" ):
                item['State_Province'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Postal Code:" ):
                item['Postal_Code'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Country:" ):
                item['Country'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Application Categories:" ):
                item['Application_Category'] = ' '.join(data_tr.xpath('following-sibling::tr/td/div[@class="divText2"]/text()').extract()).strip()

            if( data_level == "Target Industries:" ):
                item['Target_Industry'] = ' '.join(data_tr.xpath('following-sibling::tr/td/div[@class="divText2"]/text()').extract()).strip()

            if( data_level == "Key Differentiators:" ):
                item['Key_Differentiators'] = ' '.join(data_tr.xpath('following-sibling::tr/td/div[@class="divText2"]/text()').extract()).strip()

            if( data_level == "Sample Customer Names:" ):
                item['Sample_Customer_Names'] = ' '.join(data_tr.xpath('following-sibling::tr/td/div[@class="divText2"]/text()').extract()).strip()

            if( data_level == "Year Founded:" ):
                item['Year_Founded'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Public/Private Company:" ):
                item['Public_Private'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Company Phone:" ):
                item['Company_Phone'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/text()').extract()).strip()

            if( data_level == "Company Website:" ):
                item['Company_Website'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/a/@href').extract()).strip()

            if( data_level == "Company E-mail Address:" ):
                item['Company_Email'] = ' '.join(data_tr.xpath('td/div[@class="divText"]/a/text()').extract()).strip()

        yield item