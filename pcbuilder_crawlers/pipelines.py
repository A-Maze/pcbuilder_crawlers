from spiders.hardware_info import HardwareInfoSpider
from scrapy.settings import Settings
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

config = Settings()


class PcbuilderCrawlersPipeline(object):
    def __init__(self):
        self.root_url = config.get("API_URL")
        # self.api_url = ("{root_url}category/{category_name}/product"
        #                 "/{product_id}" .format(root_url=self.root_url))

    def process_item(self, item, spider):

        if spider is HardwareInfoSpider:
            self.post_item(item)
        else:
            self.post_price(item)
        return item

    def post_item(self, item):
        return item

    def post_price(self, item):
        return item
