# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
# 这里我们使用 mysql-connector-python 驱动，可以在虚拟环境下使用 pip 进行安装
import mysql.connector
import pymysql
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class ArticlespiderPipeline(object):

    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # 数据库链接
    def __init__(self):
        # 打开数据库连接
        self.conn = mysql.connector.connect(host='127.0.0.1', user='root', password='4080050346Dx', database='article_spider', use_unicode=True)
        # 使用cursor()方法获取操作游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        # SQL 插入语句
        insert_sql = """
                   insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, praise_nums, 
                   comment_nums, fav_nums, tags, content, create_date)
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = list()
        params.append(item.get('title', ''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        #  返回通过指定字符","连接序列中元素后生成的新字符串。*join()**用于将序列中的元素以指定的字符，生成一个新的字符串
        #  例如
        # l1 = ['7', '5', '4', '3', '2', '1']
        # l2 = ','.join(l1)
        # print(l2, type(l2))
        # # 7,5,4,3,2,1 <class 'str'>
        front_image = ",".join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ''))
        params.append(item.get('praise_nums', '0'))
        params.append(item.get('comment_nums', '0'))
        params.append(item.get('fav_nums', '0'))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1999-1-1'))

        self.cursor.execute(insert_sql, tuple(params))
        # 提交到数据库执行
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()


class JsonWithEncodingPipeline(object):
    #  自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("article.json", "a", encoding="utf-8")
    #  用codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode

    def process_item(self, item, spider):
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        lines = json.dumps(dict(item), ensure_ascii=False)+"\n"
        # 因为json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False：
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        # 处理结束后关闭 文件 IO 流
        self.file.closed()


class ArticlesImagePipeline(ImagesPipeline):
    #  继承并重写item_completed(),从result中获取到图片的实际下载地址
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file_path = ""
            # 通过预先设定image_file_path = ""来避免value不存在,而强行调用产生的错误
            for ok, value in results:
                #  results是一个list，每一个元素是一个turple。
                #  这个turple里面第一个值0 = True，表示是否成功。
                #  第二个值是一个字典，里面有一个键path。path的值就是文件路径。
                image_file_path = value["path"]
            item["front_image_url"] = image_file_path
        # Pipeline将从item中获取图片的URLs并下载它们，所以必须重载parse_detail(self, response)，
        # 并返回一个Request对象，这些请求对象将被Pipeline处理，
        # 当完成下载后，结果将发送到item_completed方法，
        # 这些结果为一个二元组的list，每个元祖的包含(success, image_info_or_failure)

        # 这个item是一个由Json数据：
        return item


class JsonExporterPipeline(object):
    # 初始化时指定要操作的文件, 调用scrapy提供的 json exporter 导出 json 文件
    def __init__(self):
        self.__file__ = open('articleexporte.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.__file__, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # 这个item是一个由Json数据组成的数组：
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.closed()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,  # 指定 curosr 类型
            use_unicode=True,
        )
    # 指定擦做数据库的模块名和数据库参数参数,**kwargs 表示关键字参数，它本质上是一个 dict
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)
    # 使用twisted将mysql插入变成异步执行

    def process_item(self, item, spider):
        # 指定操作方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 指定异常处理方法，报错的回调方法handle_error
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入的入库逻辑
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
                    insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, praise_nums, 
                    comment_nums, fav_nums, tags, content, create_date)
             value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url_object_id=VALUES(url_object_id)
         """
        params = list()
        params.append(item.get('title', ''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        front_image = ",".join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ''))
        params.append(item.get('praise_nums', '0'))
        params.append(item.get('comment_nums', '0'))
        params.append(item.get('fav_nums', '0'))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1999-1-1'))
        dbparms = dict(
            host='localhost',
            db='stack_db',
            user='root',
            passwd='root',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,  # 指定 curosr 类型
            use_unicode=True,
        )
        cursor.execute(insert_sql, tuple(params))
