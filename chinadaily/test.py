import requests
from bs4 import BeautifulSoup
import lxml
from pprint import pprint

url = 'http://news.qq.com/'
response = requests.get(url)
'''print(data)
print('-'*60)
print(data.text)
print('-'*60)
print(data.content)'''
soup = BeautifulSoup(response.text, 'lxml')
titleset = soup.findall()


