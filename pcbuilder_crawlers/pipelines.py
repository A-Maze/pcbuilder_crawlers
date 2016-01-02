from scrapy.settings import Settings
from template import TemplateInterface
import urllib2
import json
config = Settings()


class Pipeline(object):
    def process_item(self, item, spider):
        template = TemplateInterface()
        category = template.translate_category(item['category'])
        temp = template.get_template(category)
        item = template.translate_item(temp, item)
        json_item = json.dumps(item)
        if category is None:
            return
        self.post_item(json_item, category)

    def post_item(self, item, category):
        url = 'http://localhost:6543/category/{}/product/'.format(category)
        response = urllib2.Request(url, item)
        response.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(response)
        print resp
        return

    def post_price(self, item, category):
        return item
