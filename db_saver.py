#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


class DBSaver(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def write2db(self):
        conn = MySQLdb.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='xxxx',
            db='demo',
            charset='utf8'
        )
        cursor = conn.cursor()
        for data in self.datas:
            sql = "INSERT INTO baike_url(url,title,summary) VALUES('%s','%s','%s')"%(data['url'],data['title'],data['summary'])
            try:
                print sql
                cursor.execute(sql)
            except Exception as e:
                print 'insert into baike_url error ,url is %s'%data['url']
                conn.rollback()
                print e
            conn.commit()

        cursor.close()
        conn.close()