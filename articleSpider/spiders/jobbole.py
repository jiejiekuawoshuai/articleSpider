# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request
from articleSpider.items import JobbolespiderItem
import requests
import re
import json
from articleSpider.utils import common
# from scrapy.loader import ItemLoader
from articleSpider.items import ArticleItemLoader
#  scrapy就提供了ItemLoader这样一个容器，在这个容器里面可以配置item中各个字段的提取规则。
#  可以通过函数分析原始数据，并对Item字段进行赋值，非常的便捷。


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        # 获取新闻列表页的新闻Url并交给scrapy进行下载后调用相应的解析方法
        # 获取下一页url并交付给scrapy进行下载，下载完成后交给parse继续跟进

        post_nodes = response.css('#news_list ,news_block')[:3]
        # 获取第一页的新闻列表 ，根据网页结构搜寻网页中单个新闻图片地址以及新闻链接地址
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # next_url = response.css("div.pager a:last-child::text").extract_first("")
        # if next_url == "Next >":
        #     next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        # 提取详情页信息
    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)        # c正则表达式(.*?)惰性匹配()
        if match_re:
            # article_item = JobbolespiderItem()  # 定义items
            # title = response.css("#news_title a::text").extract_first("")  # a获取标题
            # create_data = response.css("#news_info .time::text").extract_first("")  # b 获取建立时间
            # content = response.css("#news_content").extract()[0]
            # tags_list = response.css("#guide a:last-child::text").extract()
            # tags = ",".join(tags_list)   # 转换成json对象

            post_id = match_re.group(1)
            #  d 正则表达式按照数字-字母-数字的顺序来获取相应字符串，
            # 那么分别就是“数字（group（1））–字母（group（2））–数字（group（3））”的对应关系，
            # 其中，group（0）和group（）效果相同，均为获取取得的字符串整体。
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            #
            # article_item["title"] = title
            # article_item["create_data"] = create_data
            # article_item["content"] = content
            # article_item["tags"] = tags
            # article_item["url"] = response.url
            # if response.meta.get("front_image_url", ""):
            #     article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
            # else:
            #     article_item["front_image_url"] = []
            #  下载图片注意list，因为scrapy对于article_item["front_image_url"] 中的front_image_url进行遍历
            #  response.meta.get('front_image_url','') 前一个引号是自己定义的名称，后一个空着，这样如果就不会抛异常
            #  从response meta应用get方法，若不出现需要的key，可以报错
            item_loader = ArticleItemLoader(item=JobbolespiderItem(), response=response)
            # item_loader = ItemLoader(item=JobbolespiderItem(), response=response)  # 初始化Itemloader项目加载器，
            # 可以用字典或是item作为构造函数的参数，如果没有指定， Itemloader会自己自动初始化一个item（对应属性ItemLoader.default_item_class）
            # 别忘了item=JobbolespiderItem()的括号，否则出现TypeError: items() missing 1 required positional argument: 'self'

            item_loader.add_css("title", "#news_title a::text")  # a
            item_loader.add_css("create_data", "#news_info .time::text")  # b
            item_loader.add_css("content", "#news_content")
            item_loader.add_css("tags", ".news_info .time::text")
            item_loader.add_value("url", response.url)
            item_loader.add_value("front_image_url", response.meta.get("front_image_url", ""))

            # article_item = item_loader.load_item()

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"article_item": item_loader, "url": response.url},
                          callback=self.parse_nums)
            #  yield Request进行scrapy下载逻辑

    def parse_nums(self,  response):
        j_data = json.loads(response.text)  # 得到页面字符串并进行load 成python对象
        item_loader = response.meta.get("article_item", "")
        item_loader.add_value("praise_nums", j_data["DiggCount"])
        item_loader.add_value("fav_nums", j_data["CommentCount"])
        item_loader.add_value("comment_nums", j_data["TotalView"])
        item_loader.add_value("url_object_id", common.get_md5(response.meta.get("url", "")))
        # praise_nums = j_data["DiggCount"]
        # fav_nums = j_data["CommentCount"]
        # comment_nums = j_data["TotalView"]
        # # 将所有需要的值提取出来生成我们的article_item
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["url_object_id"] = common.get_md5(article_item["url"])     #
        article_item = item_loader.load_item()
        yield article_item

        #  yield item 然后进入pipline进行一个处理，数据梳理是入库还是其他处理有由我们自己定义
# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.width = height
#
#     def __setattr__(self, name, value):
#         if name == 'size':
#             self.width, self.height = value
#         else:
#             self.__dict__(name) = value
#
#     def __getattr__(self, size):



