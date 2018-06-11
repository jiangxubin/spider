#-*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from login.items import ZimuzuItem
from scrapy import FormRequest
import re

account = 'augustus'
password = 'ZIMUZU123zimuzu'

class Zimuzu_Spider(CrawlSpider):
    name = 'zimuzu_hanguo'
    #allowed_domians = ['http://www.zimuzu.tv/']
    #start_urls = ['http://www.zimuzu.tv/User/Login']
    start_urls = 'http://www.zimuzu.tv/fresourcelist?channel=&area=%E9%9F%A9%E5%9B%BD&category=&year=&tvstation=&sort=&page=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    '''rules = (Rule(LinkExtractor(allow=('\.html',)), callback='parse_item', follow=True),)#rule itself is a tuple, argument of LinkExtractor is a tuple too

    def parse_start_url(self, response):
        formdata = {
            'account': account,
            'password': password,
            'remember': str(1),# in formdata number must be treated as str
            'url_back': "http://www.zimuzu.tv/user/user"
        }
        return [FormRequest.from_response(response, formdata=formdata, callback=self.after_login)]

    def after_login(self, response):# the argument will not be used later but it must be wrutten or bugs will occur
        print('log in successfully')
        print(response.url)
        #person_url = 'http://www.zimuzu.tv/user/fav'
        #yield Request(person_url, headers=self.headers, callback=self.parse_person_info)

    def parse_person_info(self, response):
        print(response.text)'''

    def start_requests(self):
        yield Request(self.start_urls, headers=self.headers, callback=self.parse)

    def parse(self, response):
        page_number_tag = response.xpath('*//div[@class="pages"]/div/a[last()]/@href').extract_first()
        #in xpath to indicate the last element of a list you need last() not -1
        #if you want to extract the first result of the list, use extract_first() instead of extract()
        page_number = int(re.search(r'page=(\d+)&channel', page_number_tag).group(1))
        print(page_number)
        for page in range(1, page_number+1):
        #for page in range(1, 3):
            url = 'http://www.zimuzu.tv/fresourcelist?page=' + str(page) + '&channel=&area=%E9%9F%A9%E5%9B%BD&category=&year=&tvstation=&sort=pubdate'
            print(url)
            yield Request(url, headers=self.headers, callback=self.parse_item)

    def parse_item(self, response):
        item = ZimuzuItem()
        movies = response.xpath('//div[@class="resource-showlist has-point"]/ul/li')
        for movie in movies:
            item['image_urls'] = [movie.xpath('.//div[@class="fl-img"]/a/img/@src').extract()[0]]# xpath must start with a '.' why?
            #url item should be written like this whit [] outside
            item['source_url'] = 'http://www.zimuzu.tv/' + movie.xpath('.//div[@class="fl-info"]/dl/dt/h3/a/@href').extract()[0]
            item['source_type'] = movie.xpath('.//div[@class="fl-info"]/dl/dt/h3/a/strong/text()').extract()[0]
            item['name'] = movie.xpath('.//div[@class="fl-info"]/dl/dt/h3/a/text()').extract()[0]
            yield item






