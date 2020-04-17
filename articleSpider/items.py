# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()      # TakeFirst是取第一个不为空的元素


def add_sph(value):
    return value+"sph"


def data_covert(value):
    match_re = re.match(".*?(\d+)", value)  # c正则表达式(.*?)惰性匹配()
    if match_re:
        return match_re.group(1)
    else:
        return "1970"


class JobbolespiderItem(scrapy.Item):
    # Item使用简单的class定义语法以及 Field 对象来声明。
    title = scrapy.Field()
    create_data = scrapy.Field(                  # input_processor是在收集数据的过程中所做的处理
        input_processor=MapCompose(data_covert)  # MapCompose是批量处理,传入函数的列表的每一个元素都会经过第一个函数,
    )                                            # 得到值在经过第二个函数(若有的话)，如果有返回值为None的，则抛弃。最后返回一个列表
    # input_processor一旦它通过add_xpath()，add_css()，add_value()
    # 方法收到提取到的数据便会执行，执行以后所得到的数据将仍然保存在
    # ItemLoader实例中；当数据收集完成以后，ItemLoader
    # 通过load_item()方法来进行填充并返回已填充的Item实例
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=Identity()              # output_processor是数据yield之后进行的处理
    )                                            # Identity()是取自身的函数
    front_image_path = scrapy.Field()
    comment_nums = scrapy.Field()
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(separator=",")     # 以特定字符连接，示例以空连接，对字符串也能操作
    )
    content = scrapy.Field()
    # Field类简介
    # ①Field对象指明了每个字段的元数据（任何元数据），Field对象接受的值没有任何限制
    # ②设置Field对象的主要目就是在一个地方定义好所有的元数据
    # ③注意，声明item的Field对象，并没有被赋值成class属性。（可通过item.fields进行访问）
    # ④Field类仅是内置字典类（dict）的一个别名，并没有提供额外的方法和属性。被用来基于类属性的方法来支持item生命语法。

    # define the fields for your item here like:
    # name = scrapy.Field()
