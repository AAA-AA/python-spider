#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys

import time

import db_saver
import html_downloader
import html_outputer
import html_parser
import url_manager

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderMain(object):
    #初始化爬虫模块
    def __init__(self):
        # 初始化url调度器
        self.urls = url_manager.UrlManager()
        # 初始化下载器
        self.downloader = html_downloader.HtmlDownloader()
        # 初始化解析器
        self.parser = html_parser.Parser()
        # 内容输出器
        self.outputer = html_outputer.HtmlOutputer()
        # 内容存储器
        self.saver = db_saver.DBSaver()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d :%s' % (count, new_url)
                time.sleep(1)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                self.saver.collect_data(new_data)
                if count > 1000:
                    break
                count += 1
            except:
                print 'craw failed!'
        self.saver.write2db()
        self.outputer.output_html()


if __name__ == "__main__":
    root_url = "http://baike.baidu.com/item/Python?sefr=cr"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
