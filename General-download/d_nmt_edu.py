from bs4 import BeautifulSoup
import requests
import re
from lxml import html
import os

class Pdf():
    def __init__(self, url):
        self.url = url

    def get_url(self):
        page = requests.get(self.url).text
        tree = html.fromstring(page)
        table = tree.xpath('//tr/td//@href')
        file = []
        for item in table:
            #print(item.xpath('string(.)'))#this is the way to change the element to string
            if not re.search(r'/', item):
                os.chdir('E:/fluid/')
                full_url = r'http://infohost.nmt.edu/~petro/faculty/Engler571/' + item  # - can't be used _ shoud be used instead
                file.append(item)
                content = requests.get(full_url).content
                print(full_url)
                name = item
                with open(name, 'wb+') as f:
                    f.write(content)

pdf = Pdf('http://infohost.nmt.edu/~petro/faculty/Engler571/?C=N;O=D')
pdf.get_url()
