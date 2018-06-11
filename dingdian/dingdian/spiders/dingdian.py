import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem

class Myspider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains = ['23wx.cc']
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
    bash_url = 'http://m.23wx.cc/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse, headers=self.headers)
        yield Request('http://m.23wx.cc/quanben/1/', callback=self.parse, headers=self.headers)

    def parse(self, response):
        page_tag = response.xpath('//div[@class="page"]//@href').extract()[-1]
        #print(page_tag)
        page_number = int(re.search(r'_(\d+)', page_tag).group(1))
        #print(page_number)
        class_number = int(re.search(r'(\d+)_', page_tag).group(1))
        #print(class_number)
        for i in range(1, int(page_number)+1):
            per_url = self.bash_url + str(class_number) + '_' + str(i) + self.bashurl
            print(per_url)
            yield Request(per_url, headers=self.headers, callback=self.get_name)

    def get_name(self, response):
        book_tags = response.xpath('//div[@class="cover"]/p/a[@class="blue"]').extract()
        for book_tag in book_tags:
            novel_url = re.search(r'href="(.*?)" class', book_tag).group(1)
            novel_name = re.search(r'>(.*?)</a>', book_tag).group(1)
            novel_url = str('http://m.23wx.cc') + str(novel_url) #+ '/'查看目录
            #print(novel_name, novel_url)
            yield Request(novel_url, headers=self.headers, callback=self.get_chapter, meta={'novel_name': novel_name, 'novel_url': novel_url})#上面已经改完了

    def get_chapter(self, response):
        item = DingdianItem()
        item['name'] = response.meta['novel_name']
        item['novelurl'] = response.meta['novel_url']
        print(item['name'], item['novelurl'])
        author = response.xpath('//div[@class="block_txt2"]/p/a').extract()[1]
        author = re.search(r'>(.*?)</a>', author).group(1)
        print(author)
        category = response.xpath('//div[@class="block_txt2"]/p/a').extract()[2]
        category = re.search(r'>(.*?)</a>', category).group(1)
        print(category)
        name_id = str(response.url.split(r'/')[-1])
        print(name_id)
        item['author'] = str(author)
        item['category'] = str(category)
        item['name_id'] = str(name_id)
        yield item




