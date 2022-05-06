from logging import exception
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime


class WineSpider(CrawlSpider):
    name = 'wine'
    allowed_domains = ['www.foodandwine.com']
    start_urls = [
        'https://www.foodandwine.com/news?page=1',
        'https://www.foodandwine.com/news?page=2'
        ]


    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//main/div[7]/div/div[3]/div/div[2]/a"), 
            callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        title = response.xpath("//h1/text()").get()
        date = response.xpath("//span[@class='byline__block byline__block--timestamp']/text()").get().replace(' ','-').replace(',','')
        try:
            date = datetime.strptime(str(date), "%b-%d-%Y")
        except Exception as e:
            date = datetime.strptime(str(date), "%B-%d-%Y")

        if title != None:
            yield {
                'Title':title,
                'Publication_date': date,
            }
        

