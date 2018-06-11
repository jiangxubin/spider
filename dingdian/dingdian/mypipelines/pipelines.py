from .sql import Sql
from dingdian.items import DingdianItem

class DingdianPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DingdianItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret == 1:
                print('已经存在')
                pass
            else:
                xs_name = item['name']
                xs_author = item['author']
                category  = item['category']
                Sql.insert__dd_name(xs_name, xs_author, category, name_id)
                print('开始存储小说信息')