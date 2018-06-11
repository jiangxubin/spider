#-*- coding:utf-8 -*-
#import download
from bs4 import BeautifulSoup
import re
import os
from modified_request import download

def article(url):
    wbdata = download.get(url).text
    soup = BeautifulSoup(wbdata, 'lxml')
    if soup.find('div', id="Content") == None:#文章内容是否存在
        print('this article link is blank,continue to next one, and you need to delete this link from the database')
    else:
        if soup.find('div', id="div_currpage") == None:#通过页面标签判断是否只有一页
            print('this article has only one page')
            para_get(url)
        else:
            print('this article has more than one page')
            page = 1
            page_total = page_count(url)
            while page <= page_total:
                if page == 1:
                    para_get(url)
                    print("this is %d page" % page)
                    page += 1
                else:
                    print('this is %d page' % page)
                    list_url = list(url)
                    list_url.insert(-4, '_'+str(page))
                    list_url = ''.join(list_url)
                    para_get(list_url)
                    page += 1

def page_count(url):
    wbdata = download.get(url).text
    soup = BeautifulSoup(wbdata, 'lxml')
    if soup.find('div', id="div_currpage") == None:
        total_page = int(1)
        print('this article has %d page' % total_page)
        return total_page
    else:
        page_tag = soup.select("div#div_currpage a.pageno")
        total_page = int(page_tag[-1].string)
        print('this article has %d page' % total_page)
        page_tag = soup.select("div#div_currpage a")
        total_page = int(page_tag[-2].string)
        return total_page

def para_get(url):
    wbdata = download.get(url).text
    soup = BeautifulSoup(wbdata, 'lxml')
    paragraph = soup.find('div', id="Content").find_all('p')
    #corpus_path = r"F:/repository/Corpus.txt"
    if os.path.exists("F:/repository/corpus.txt"):
        os.chdir("F:/repository/")
        pass
    else:
        with open("Corpus.txt", 'w', encoding='utf-8') as file:
            file.close()
        os.chdir("F:/repository/")#chdir是改变工作目录的，不能切换到一个文件下去
    for p_tag in paragraph:
        duanluo = p_tag.get_text()
        duanluo = re.sub(r'\[.*?\]', ' ', str(duanluo))  # 去除[]本身必须使用\转意符号，去除[]及其所包含的内容并以空格替代
        duanluo = re.sub(r'[,?!."]', ' ', duanluo)  # 去除符号
        duanluo = re.sub(r'\(.*?\)', ' ', duanluo)  # 去除（）及其所包含的内容
        duanluo = re.sub(r'\n', ' ', duanluo)#去除换行
        duanluo = duanluo.lower()
        duanluo = duanluo.split()
        duanluo = [danci for danci in duanluo]
        duanluo = ' '.join(duanluo)
        with open("F:\\repository\\Corpus.txt", mode='a+', encoding='utf-8') as file:
            file.write(duanluo+'\n')
        print(duanluo)




