#coding: utf-8
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pymysql

url = 'http://www.chaojibiaoge.com/index.php/System/Model/getData?modelid=oa_sheet&filter=(projectid%3D%3CDYH%3E17041217070420049240%3CDYH%3E)&orderby=sort&page=1&pagerows=24&rowCount=200&view_id=&searchword=&sql=&fromRow=0&getRecordCount=true&usermodel_recordid=17041217070420049240&model_ownerid=tjustt'
data = requests.get(url).text
result = json.loads(data)
#pprint(result)
for key in result.keys():
    print(key)
infolist = result['rows']
pprint(type(infolist))
pprint(infolist[12])
conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='usbw', charset='utf8')
cursor = conn.cursor()
#create database
#dbname = 'TEST'
cursor.execute("DROP DATABASE IF EXISTS `test`")
cursor.execute("CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci")
conn.select_db('test')
cursor.execute("CREATE TABLE `infoset`(id INT auto_increment,studentname VARCHAR (100),birthday VARCHAR (100),birthlocation VARCHAR (200),oldphone VARCHAR (200),newphone VARCHAR (200),teacher VARCHAR (200),bachelor VARCHAR (200),discipline VARCHAR (200),pici VARCHAR (200),degree VARCHAR (200),job VARCHAR (200),huji VARCHAR (200),joblocation VARCHAR (200),PRIMARY KEY (id))DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci")
for item in infolist:
    studentname = item['SYS_string6'],
    print(studentname)
    birthday =item['SYS_string7'],
    print(item['SYS_string7'],type(birthday))
    birthlocation = item['SYS_string8'],
    print(birthlocation),
    oldphone = item['SYS_string19'],
    print(oldphone),
    newphone = item['SYS_string18'],
    print(newphone),
    teacher = item['SYS_string10'],
    print(teacher)
    bachelor = item['SYS_string11'],
    print(bachelor)
    discipline = item['SYS_string12'],
    print(discipline)
    pici = item['SYS_string13'],
    print(pici)
    degree = item['SYS_string14'],
    print(degree)
    job = item['SYS_string15'],
    print(job)
    huji = item['SYS_string16'],
    print(huji)
    joblcation = item['SYS_string17'],
    print(joblcation)
    cursor.execute("insert into `infoset`(studentname,birthday,birthlocation,oldphone,newphone,teacher,bachelor,discipline,pici,degree,job,huji,joblocation)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(item['SYS_string6'],item['SYS_string7'],item['SYS_string8'],item['SYS_string19'],item['SYS_string18'],item['SYS_string10'],item['SYS_string11'],item['SYS_string12'],item['SYS_string13'],item['SYS_string14'],item['SYS_string15'],item['SYS_string16'],item['SYS_string17']))#right operator
    #cursor.execute("insert into `infoset`(studentname)VALUES ('{0}')" .format(strname))#wrong operator,why?
    conn.commit()
cursor.close()
conn.close()