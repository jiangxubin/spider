#-*- coding:utf-8 -*-
#import
from bs4 import BeautifulSoup
import re
import pymysql
import article_content_crawler as content
from modified_request import download

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', db='chinadaily', password='usbw', charset='utf8')
cursor = conn.cursor()
'''cursor.execute('DROP DATABASE IF  EXISTS chinadaily')
cursor.execute('CREATE DATABASE IF NOT EXISTS chinadaily ')
cursor.execute('DROP TABLE IF EXISTS LINKSET')
cursor.execute('CREATE TABLE LINKSET(id INT auto_increment PRIMARY KEY ,pagelink VARCHAR (200))')'''

start_url = 'http://www.chinadaily.com.cn/'
visited = []
todo = []
article = []
host = start_url.split('/')
print(host[2])

def get_all_link(page):
    wbdata = download.get(page).text
    soup = BeautifulSoup(wbdata, 'lxml')
    atagset = soup.find_all('a')
    for atag in atagset:
        #link = atag['href']#it may be wrong
        link = str(atag.get('href'))#获取链接地址
        #print(link)
        link = link_filter(link)#对链接地址进行过滤并返回修改值
        print(link)
        if link:#若链接不为空
            if link in visited:#如果链接已访问过
                print('this link existed')
                continue#进行下一个链接爬取
            else:#链接未访问过
                link_type(link)
        else:
            continue


def link_filter(url):
    pattern0 = re.compile(r'javascript')
    pattern1 = re.compile(r'\s')
    pattern2 = re.compile(r'jpg$')
    pattern3 = re.compile(r'/m/')
    if re.search(pattern0, url):
        print("this link is a javascript")
        return None
    elif re.search(pattern1, url):
            print("this link is blank")
            return None
    elif re.search(pattern2, url):
        print('this link is a img')
        return None
    elif re.search(pattern3, url):
        print('this link is for mobile')
        return None
    elif url.startswith('http'):
        if url.split('/')[2] == host[2]:
            print("this is the link which matches our goal and needs no modification")
            return url
        else:
            print("this link doesn't match our goal,because it is linked to outside website")
            return None
    else:
        url = 'http://www.chinadaily.com.cn/' + url
        print("this link is our goal, but we need to add some string to complete it")
        return url


def link_type(url):
    pattern_article = re.compile(r'content')
    if re.search(pattern_article, url):
        print('this link is article link')
        article.append(url)
        visited.append(url)
        if cursor.execute('select * from LINKSET WHERE pagelink="%s"'%(url)) == 0:
            cursor.execute('INSERT INTO LINKSET(pagelink) VALUES ("%s")' %(url))
            conn.commit()#必须提交 否则数据库为空
        else:
            print('this link exists')
        print(len(article), len(visited))
    else:
        visited.append(url)
        print(len(visited))
        print('this link still needs to be crawled')
        get_all_link(url)

def link_crawler():
    print('now the script is going to get all the article link from china_daily,please wait ')
    print('the script is crawling link')
    #get_all_link(start_url)
    print('all links have been crawled and stored in the data_base:chinadaily')
    print('now the script is going to fetch article link from the database and store the content in a txt file')
    cursor.execute('select pagelink from linkset')
    data = cursor.fetchall()
    #print(type(result), type(data))
    for item in data:
        href = item[0]
        #print(item)
        #print(item[0])#返回结果都是元祖，不想用（'',）这种数据就要使用[0]的方式获取字符串数据
        try:
            content.article(href)
        except IndexError:
            continue


#get_all_link(start_url)
link_crawler()
#get_all_link(start_url)
cursor.close()
conn.close()
#print(todo)
#print(article)





