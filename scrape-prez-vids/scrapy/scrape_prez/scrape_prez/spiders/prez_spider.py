import scrapy
import os
import shutil
import logging
import pickle as pk
from scrapy_splash import SplashRequest
from scrape_prez.items import prezItem
import unidecode

# to crawl: scrapy crawl prez -o output.prez.json

# scrapy shell notes:
# newUrl = baseUrl + response.xpath('//h3[contains(@class, "field-content")]/a/@href').extract()[0]
# fetch(newUrl)
## gets speech text:
# response.xpath("//div[contains(@class, 'field-item')]").extract()
# speechText = response.xpath("//div[contains(@class, 'field-item even')]/p//text()").extract()
# speechTextOne = ' '.join(speechText)
# end of metadata signalled by "\n\t\xa0"



# search for something with class name: response.xpath('//h3[contains(@class, "field-content")]')
# get all links to addresses: response.xpath('//h3[contains(@class, "field-content")]/a/@href').extract()
# http://stackoverflow.com/questions/1604471/how-can-i-find-an-element-by-css-class-with-xpath
# http://doc.scrapy.org/en/latest/topics/selectors.html

# scolling down:
# https://www.whitehouse.gov/briefing-room/weekly-address?page=1

baseUrl = 'https://www.whitehouse.gov'

weeklyUrl = baseUrl + '/briefing-room/weekly-address' # 'https://www.whitehouse.gov/briefing-room/weekly-address'

urls = [weeklyUrl] + [weeklyUrl + '?page=' + str(i) for i in range(1, 40)]

# test with
# scrapy shell 'https://www.whitehouse.gov/briefing-room/weekly-address'
# response.xpath('//h3[contains(@class, "field-content")]/a/@href').extract()

class prezSpider(scrapy.Spider):
    name = "prez"
    allowed_domains = ["whitehouse.gov"]
    start_urls = urls

    '''def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 0.5})
    '''

    def parse(self, response):
        # finds element by class name:
        # response.xpath("//a[contains(@class, 'transcript-toggle')]/text()").extract()
        for address in response.xpath('//h3[contains(@class, "field-content")]/a/@href').extract():
            item = prezItem()
            item['weekly_address_url'] = baseUrl + address
            #yield item
            yield scrapy.Request(baseUrl + address, callback=self.parse_addr, meta={'item': item})
            '''item['desc'] = sel.xpath('div/p/text()').extract()
            item['link'] = sel.xpath('div/h2/a/@href').extract()
            url = sel.xpath('div/a/img/@src').extract()
            if len(url) == 1:
                #self.logger.warning('url:' + str(url[0][2:]))
                item['image_urls'] = ['http://' + url[0][2:]]
                #item['files'] = item['breed']
            isempty = True
            for k, v in item.items():
                if v == []:
                    continue
                else:
                    yield item
            '''
    def parse_addr(self, response):
        item = response.meta['item']
        title = unidecode.unidecode(response.xpath("//h1//text()").extract()[0])
        if title[:14] == 'Weekly Address':
            vidLink = response.xpath("//a[contains(@class, 'link-mp4')]/@href").extract()
            if vidLink != []:
                rawText = unidecode.unidecode(' '.join(response.xpath("//div[contains(@class, 'field-item even')]/p//text()").extract()))
                #speechText =
                item['rawText'] = rawText
                # example of getting video link:
                # scrapy shell "https://www.whitehouse.gov/the-press-office/2016/08/27/weekly-address-taking-action-against-zika-virus"
                # response.xpath("//a[contains(@class, 'link-mp4')]/@href").extract()
                # this next line will download all the files in the item['file_urls']

                item['videoLink'] = vidLink[0]
                item['file_urls'] = vidLink
                item['speechTitle'] = title[16:]
                yield item
