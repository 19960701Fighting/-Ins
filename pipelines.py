# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# class InsSpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymysql
class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='123456',
            db='instagram',
            port=3306,
            use_unicode=True,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO tables(username, display_url, text, comment)VALUES(%s, %s, %s, %s)"
        self.cursor.execute(sql, (item['username'], item['display_url'], item['text'], item['comment']))
        self.conn.commit()
        return item

    def close_spider(self):
        self.cursor.close()
        self.conn.close()


# class CustomImagePipeline(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         # 将item放入request中
#         reqs = [Request(x, meta={'item': item}) for x in item.get(self.images_urls_field, [])]
#         for r in reqs:
#             r.headers.setdefault('Referer', item['referer'])
#             r.headers.setdefault('Accept', '*/*')
#             r.headers.setdefault('Host', 'www.instagram.com')
#             r.headers.setdefault('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
#             r.headers.setdefault('Accept-Encoding', 'gzip, deflate, br')
#             r.headers.setdefault('Connection', 'keep-alive')
#             r.headers.setdefault('Cookie', 'csrftoken=4aK38rcjjcvkQzUvxet3Txu2EPEJ9zjA; ig_cb=1; rur=FRC; mid=W5djwgAEAAFVjBl7jMR9_4YPoxbm; mcd=3; csrftoken=4aK38rcjjcvkQzUvxet3Txu2EPEJ9zjA; ds_user_id=8567823641; urlgen="{\"178.128.117.45\": 14061}:1fzh15:VI7mCN1gCLQAWydbs2njTwpm8u8"; sessionid=IGSCf4b68323e98ac53ff8ed6aa0b504706c2abc24834bd70155c456f5b61d66b9c6%3ADVwPsw4ErirJ34BQisq9TjE597mgbW45%3A%7B%22_auth_user_id%22%3A8567823641%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228567823641%3ANG6da1zgaKq1nwFYiuDVLqdHJXbMyZ3A%3A4551d64f086ef07fbfb592eaf4c5ce0c9ab670104d9e9f79d3a92c52da88bfe2%22%2C%22last_refreshed%22%3A1536648161.4038498402%7D')
#
#         return reqs

    # def file_path(self, request, response=None, info=None):
    #
    #     item = request.meta.get('item')
    #
    #     author = item['author'].strip().strip('/')
    #
    #     # 拼接图片最终存放的路径
    #     path = author + '.jpg'
    #
    #     return path