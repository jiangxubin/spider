import requests
from lxml import etree
import os
import codecs
from threading import Thread
import re
import time
'''response = requests.get('http://blog.sina.com.cn/s/blog_4a6b74cd010178ty.html')
#print(response.encoding)#如果网页出现奇怪的乱码，可以使用这个查看网页编码方式
response.encoding = 'utf-8'
tree = etree.HTML(response.text)
content = tree.xpath('//div[@id="sina_keyword_ad_area2"]/div|//div[@id="sina_keyword_ad_area2"]/p')'''
'''for item in content:
    if item.tag == 'div':
        if item.xpath('.//a'):
            href = str(item.xpath('.//a/@href')[0] + u'\n')
            print(href)
        else:
            p_original = item.xpath('.//text()')
            p_modified = []
            for sentence in p_original:
                p_modified.append(sentence)
            p_striped = str(''.join(p_modified) + u'\n')
            print(p_striped)
    elif item.tag == 'p':
        if item.xpath('.//a'):
            href = str(item.xpath('.//a/@href')[0] + u'\n')
            print(href)
        else:
            p_original = item.xpath('.//text()')
            p_modified = []
            for sentence in p_original:
                p_modified.append(sentence)
            p_striped = str(''.join(p_modified) + u'\n')
            print(p_striped)'''


def get_blog_url_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    tree = etree.HTML(response.text)
    url_list = tree.xpath('//div[@class="articleList"]//span[@class="atc_title"]//@href')
    return url_list


def get_blog_content(blog_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    response = requests.get(blog_url, headers=headers)
    response.encoding = 'utf-8'
    blog_tree = etree.HTML(response.text)
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
                #print(href)
            else:
                p_original = p.xpath('.//text()')
                p_modified = []
                for sentence in p_original:
                    sentence = sentence_trip(sentence)
                    p_modified.append(sentence)
                p_striped = str(''.join(p_modified) + u'\n')
                f.write(p_striped)
                #print(p_striped)
        elif p.tag == 'p':
            if p.xpath('.//a'):
                href = str(p.xpath('.//a/@href')[0] + u'\n')
                f.write(href)
                #print(href)
            else:
                p_original = p.xpath('.//text()')
                p_modified = []
                for sentence in p_original:
                    sentence = sentence_trip(sentence)
                    p_modified.append(sentence)
                p_striped = str(''.join(p_modified) + u'\n')
                f.write(p_striped)
                #print(p_striped)
    f.close()


def sentence_trip(sentence):
    sentence = re.sub(u'\xa0', u' ', sentence)
    sentence = re.sub(u'\n', u' ', sentence)
    return sentence

blog_url_list = get_blog_url_list('http://blog.sina.com.cn/s/articlelist_1248556237_0_15.html')
start = time.time()
print('start time is {0}'.format(start))
for url in blog_url_list:
    thread = Thread(target=get_blog_content, args=(url, ))
    thread.start()
    print('threading{0} is dowanloading {1}'.format(os.getpid(), url))
    thread.join()
end = time.time()
print('end time is {0}'.format(end))
print('whole time is {0}'.format(end - start))
