import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pymysql
url = 'https://www.toutiao.com/api/pc/focus/'
data = requests.get(url).text
result = json.loads(data)
pprint(type(result))
news = result['data']['pc_feed_focus']
conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='usbw', charset='utf8')
cursor = conn.cursor()
#db = 'jrtt'
cursor.execute("drop database if EXISTS `jrtt`")
cursor.execute("create database if NOT EXISTS `jrtt` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci")
conn.select_db('jrtt')
#tb = 'info'
cursor.execute("create table `info`(title VARCHAR(100) ,link VARCHAR(100) ,imglink VARCHAR(100) )DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci")
for item in news:
    print(type(item))
    title = item['title']
    print(type(title))
    url = item['media_url']
    img_url = item['image_url']
    cursor.execute("insert into `info`(title,link,imglink)VALUES('{0}','{1}','{2}')".format(title,url,img_url))
    conn.commit()


cursor.close()
conn.close()