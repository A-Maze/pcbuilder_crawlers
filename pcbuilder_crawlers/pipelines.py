from scrapy.settings import Settings
from template import TemplateInterface
import urllib2
import json
config = Settings()


class Pipeline(object):
    def process_item(self, item, spider):

        template = TemplateInterface()
        category = template.translate_category(item['category'])
        if spider.name == 'hardwareinfo':
            temp = template.get_template(category)
            item = template.translate_item(temp, item)
            json_item = json.dumps(item)
            self.post_item(json_item, category)
        else:
            temp = template.get_template('record')
            item = template.translate_item(temp, item)
            json_item = json.dumps(item)
            self.post_price(json_item, category)

    def post_item(self, item, category):
        url = 'http://localhost:6543/category/{}/product/'.format(category)
        response = urllib2.Request(url, item)
        response.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(response)
        print resp
        return {
            "message": "item posted"
        }

    def post_price(self, item, category):
        url = 'http://localhost:6543/category/{}/record/'.format(category)
        print url
        response = urllib2.Request(url, item)
        response.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(response)
        print resp
        return {
            "message": "price posted"
        }
