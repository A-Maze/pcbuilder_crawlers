# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests

class PcbuilderCrawlersPipeline(object):

    def process_item(self, item, spider):
        """ translate the json keys """

        #make the request
        url = 'http://95.85.12.99/' + item['category'] + '/product'
        r = requests.post(url, item)
        return item
