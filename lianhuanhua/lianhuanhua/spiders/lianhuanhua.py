from scrapy.http import Request
from scrapy.spider import Spider
from lianhuanhua.items import LianhuanhuaItem
import os
import re
import requests
import pdb

class LianhuanhuaSpider(Spider):
    name = 'lianhuanhua'
    #allowed_domains = ['http://finance.ifeng.com']
    handle_httpstatus_list = [404]
    base_url = 'http://finance.ifeng.com/picture/special/picture'
    page_count = 181
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    error_list = []

    def start_requests(self):
        start_url = self.base_url + str(self.page_count) + r'/'
        print(start_url)
        yield Request(start_url, callback=self.parse)

    def parse(self, response):
        path = 'G:/Scrapy/lianhuanhua/pictures/'
        try:
            pic_urls_test = response.xpath('//div[@class="pic01"]/div/img/@src').extract()[0]
        except IndexError:
            error_url = response.url
            print(error_url, "这一链接页面不存在")
            self.error_list.append(error_url)
            error_page_count = error_url[-4:-1]
            print(error_page_count, "第%s期不存在"%error_page_count)
            self.page_count = int(error_page_count) + 1
            print(self.page_count, "即将爬取下一期:%s"%self.page_count)
            next_url = self.base_url + str(self.page_count) + r'/'
            print(next_url)
            yield Request(next_url, callback=self.parse)

        pic_urls = response.xpath('//div[@class="pic01"]/div/img/@src').extract()
        episode = response.url[-4:-1]
        print("这一期号为：%s"%episode)
        absolute_path = os.path.join(path, episode)
        if os.path.exists(absolute_path):
            print(self.page_count, "这期：%s已经存在于本地磁盘"%self.page_count)
            self.page_count += 1
            print(self.page_count, "即将爬取下一期:%s"%self.page_count)
            next_url = self.base_url + str(self.page_count) + r'/'
            yield Request(next_url, callback=self.parse)
        else:
            if len(pic_urls) >= 2:
                os.chdir(path)
                os.makedirs(episode)
                absolute_path = os.path.join(path, episode)
                os.chdir(absolute_path)
                for pic_url in pic_urls:
                    name = pic_url[-19:-5]
                    print("正在写入的图片名为%s"%name)
                    img = requests.get(pic_url, headers=self.headers)
                    f = open(name + '.jpg', 'ab')
                    f.write(img.content)
                    f.close()
                    self.page_count += 1
            else:
                os.chdir(path)
                os.makedirs(episode)
                absolute_path = os.path.join(path, episode)
                os.chdir(absolute_path)
                pic_url = pic_urls[0]
                name = pic_url[-19:-5]
                print("正在写入的图片名为%s"%name)
                img = requests.get(pic_url, headers=self.headers)
                f = open(name + '.jpg', 'ab')
                f.write(img.content)
                f.close()
                self.page_count += 1
            next_url = self.base_url + str(self.page_count) + r'/'
            yield Request(next_url, callback=self.parse)


