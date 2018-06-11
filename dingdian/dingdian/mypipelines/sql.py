#-*-conding;utf-8 -*-
import pymysql
from dingdian import settings
import pdb

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

conn = pymysql.connect(host=MYSQL_HOSTS, user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT, database=MYSQL_DB)#必须加上默认字符集为utf8
cursor = conn.cursor()
conn.set_charset('utf8')#貌似最终就是在这里设置了数据库的编码格式，加上在mysql里设置一下字段的编码类型

class Sql(object):
    #pdb.set_trace()
    @classmethod
    def insert__dd_name(cls, xs_name, xs_author, category, name_id):
        sql = 'INSERT INTO dd_name (xs_name, xs_author, category, name_id) VALUES (N%(xs_name)s, N%(xs_author)s, N%(category)s, N%(name_id)s)'#利用字典进行格式化输出
        value = {
            'xs_name': xs_name,
            'xs_author': xs_author,
            'category': category,
            'name_id': name_id
        }
        cursor.execute(sql, value)#cursor游标执行查询命令
        conn.commit()#conn连接执行提交命令

    @classmethod
    def select_name(cls, name_id):
        sql = 'SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)'
        value = {
            'name_id': name_id
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]


