# coding=utf-8
import datetime
import json
import time

import redis
import scrapy
from pymongo import MongoClient
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider

from biliob_spider.items import TagListItem
from biliob_tracer.task import SpiderTask
from db import db, settings
from mail import mailer


class TagAdderSpider(RedisSpider):
    name = "tagAdder"
    allowed_domains = ["bilibili.com"]

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'biliob_spider.pipelines.TagAdderPipeline': 300
        },
    }
    def __init__(self):
        self.client = MongoClient(settings['MINGO_HOST'], 27017)
        # 数据库登录需要帐号密码
        self.client.admin.authenticate(settings['MINGO_USER'],
                                     settings['MONGO_PSW'])
        self.db = self.client['biliob']  # 获得数据库的句柄
        self.task = SpiderTask('视频标签追加爬虫', collection=self.db['tracer'])
        pass

    def parse(self, response):
        pass
        try:
            self.task.crawl_count += 1
            aid = str(
                response.url.lstrip(
                    'https://www.bilibili.com/video/av').rstrip('/'))
            tagName = response.xpath("//li[@class='tag']/a/text()").extract()
            item = TagListItem()
            item['aid'] = int(aid)
            item['tag_list'] = []
            if tagName != []:
                ITEM_NUMBER = len(tagName)
                for i in range(0, ITEM_NUMBER):
                    item['tag_list'].append(tagName[i])
            yield item
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
            item = TagListItem()
<<<<<<< HEAD
            item['aid'] = int(aid)
            item['tag_list'] = []
            yield item
=======
            item['tag_name'] = ''
            print(response.url)
>>>>>>> ccbc48ffa2e158f353a8174aa02f6160e68a8575