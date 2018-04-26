#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-04-26 10:52:48
# Project: wechat

from pyspider.libs.base_handler import *
import pymongo


class Handler(BaseHandler):
    start_url = 'http://weixin.sogou.com/weixin?'
    query = {
        'query': 'python',
        'type': 2,
        'page': 1,
        'ie': 'utf8',
    }
    client = pymongo.MongoClient("localhost")
    db = client['wechat']
    crawl_config = {

    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(Handler.start_url, callback=self.index_page, params=Handler.query, method="GET")

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.news-box .news-list li .txt-box h3 a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        if response.doc('.p-fy .np').attr.href:
            self.crawl(response.doc('.p-fy .np').attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        author = response.doc('.rich_media_meta_link').text()
        wechat = response.doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        content = response.doc('#js_content').text()
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            'author': author,
            'wechat': wechat,
            'content': content,
        }

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        if self.db["articles"].insert(result):
            print("save to mongodb sucess", result)