# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
# import json
import re
import locale
import psycopg2
from datetime import datetime

class MangaPipeline(object):
    # def __init__(self):
    #     self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        conn = psycopg2.connect("dbname=mydb")
        cur = conn.cursor()
        locale.setlocale(locale.LC_TIME, "fr_FR")
        if item['tome']:
            for x in item['tome']:
                if 'Tome' in x:
                    item['tome'] = [x[9:]]
                else:
                    raise DropItem("Missing price in %s" % item)
        if item['release_date']:
            for x in item['release_date']:
                if 'Sortie' in x:
                    x = x.encode('utf8')
                    new_date = unicode(str(datetime.date(datetime.strptime(x[10:] ,'%d %B %Y'))))
                    item['release_date'] = [new_date]
        if item['name']:
            for x in item['name']:
                item['name'] = [re.sub(r'\s[tT]\d{2}', '', x)]
        if item['cover']:
            for x in item['cover']:
                if 'provisoire' in x:
                    item['cover'] = ['']
                else:
                    item['cover'] = [x[:-14]]
        cur.execute("INSERT INTO pika (name, cover, collection, tome, release_date) VALUES (%s, %s, %s, %s, %s)", (item['name'][0], item['cover'][0], item['collection'][0], item['tome'][0], item['release_date'][0]))
        conn.commit()
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)
        cur.close()
        conn.close()
        return item
