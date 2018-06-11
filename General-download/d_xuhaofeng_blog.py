#-*-coding:utf-8-*-
import requests
import re
from lxml import etree
import os
import codecs
class Blog():
    def __init__(self, url):
        self.url = url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    def get_tree(self, url):
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)
        return tree

    def get_blog_url_list(self, tree):
        url_list = tree.xpath('//div[@class="articleList"]//span[@class="atc_title"]//@href')
        return url_list

    def get_page_count(self):
        tree = self.get_tree(self.url)
        page_count = tree.xpath('//div[@class="SG_page"]//span/text()')
        page_count = page_count[0][1:3]
        return int(page_count)

    def get_all_pages(self):
        page_count = self.get_page_count()
        for i in range(1, page_count+1):
            page_url = 'http://blog.sina.com.cn/s/articlelist_1248556237_0_' + str(i) + '.html'
            print(page_url)
            page_tree = self.get_tree(page_url)
            blog_url_list = self.get_blog_url_list(page_tree)
            for blog_url in blog_url_list:
                blog_tree = self.get_tree(blog_url)
                self.get_blog_content(blog_tree)

    def get_blog_content(self, blog_tree):
        os.chdir('G:/projects/General/xuhaofeng/')
        blog_title = str(blog_tree.xpath('//div[@class="articalTitle"]/h2//text()')[0])
        f = codecs.open(blog_title + '.md', 'w', encoding='utf-8')
        f.write(blog_title + u'\n')
        print(blog_title)
        blog_content = blog_tree.xpath('//div[@id="sina_keyword_ad_area2"]/p|//div[@id="sina_keyword_ad_area2"]/div')
        for p in blog_content:
            if p.tag == 'div':
                if p.xpath('.//a'):
                    href = str(p.xpath('.//a/@href')[0] + u'\n')
                    f.write(href)
                    print(href)
                else:
                    p_original = p.xpath('.//text()')
                    p_modified = []
                    for sentence in p_original:
                        sentence = self.sentence_trip(sentence)
                        p_modified.append(sentence)
                    p_striped = str(''.join(p_modified) + u'\n')
                    f.write(p_striped)
                    print(p_striped)
            elif p.tag == 'p':
                if p.xpath('.//a'):
                    href = str(p.xpath('.//a/@href')[0] + u'\n')
                    f.write(href)
                    print(href)
                else:
                    p_original = p.xpath('.//text()')
                    p_modified = []
                    for sentence in p_original:
                        sentence = self.sentence_trip(sentence)
                        p_modified.append(sentence)
                    p_striped = str(''.join(p_modified) + u'\n')
                    f.write(p_striped)
                    print(p_striped)
        f.close()

    def sentence_trip(self, sentence):
        sentence = re.sub(u'\xa0', u' ', sentence)
        sentence = re.sub(u'\n', u' ', sentence)
        return sentence

if __name__ == '__main__':
    Xuhaofeng_blog = Blog('http://blog.sina.com.cn/s/articlelist_1248556237_0_1.html')
    Xuhaofeng_blog.get_all_pages()