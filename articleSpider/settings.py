# -*- coding: utf-8 -*-
import os
import sys
# Scrapy settings for articleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'articleSpider'

SPIDER_MODULES = ['articleSpider.spiders']
NEWSPIDER_MODULE = 'articleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'articleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'articleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'articleSpider.middlewares.ArticlespiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 指定用来处理数据的 Pipeline 类，后面的数字代表执行顺序,取值范围是  0-1000 range.
# 数值小的 Pipeline 类优先执行
ITEM_PIPELINES = {
   'articleSpider.pipelines.ArticlespiderPipeline': 300,
   'articleSpider.pipelines.ArticlesImagePipeline': 1,
   'articleSpider.pipelines.JsonWithEncodingPipeline': 2,
   'articleSpider.pipelines.JsonExporterPipeline': 3,
   'articleSpider.pipelines.MysqlTwistedPipeline': 4,
   # 'articleSpider.pipelines.MysqlPipeline': 5
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#  设定item中哪个是图片下载地址(IMAGES_URLS_FIELD)，文件夹的相对路径，文件下载存储目录（IMAGES_STORE）
IMAGES_URLS_FIELD = "front_image_url"
project_dir = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'article_spider'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '4080050346Dx'
