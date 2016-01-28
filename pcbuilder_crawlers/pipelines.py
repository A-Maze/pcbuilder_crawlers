import redis
from scrapy.settings import Settings
from template import TemplateInterface
import urllib2
import json
config = Settings()


class Pipeline(object):
    def __init__(self):
        self.root_url = config.get("API_URL")
        self.redis_port = config.get("REDIS_PORT")

        case = []
        cooler = []
        cpu = []
        hard_drive = []
        memory = []
        motherboard = []
        optical_drive = []
        power_supply = []
        video_card = []
        self.items = [case, cooler, cpu, hard_drive, memory,
                      motherboard, optical_drive, power_supply, video_card]
        self.category_names = ['case', 'cooler', 'cpu', 'hard_drive', 'memory',
                               'motherboard', 'optical_drive', 'power_supply',
                               'video_card']
        self.category_list_mapping = {
            'case': 0,
            'cooler': 1,
            'cpu': 2,
            'hard_drive': 3,
            'memory': 4,
            'motherboard': 5,
            'optical_drive': 6,
            'power_supply': 7,
            'video_card': 8
        }

    def process_item(self, item, spider):

        template = TemplateInterface()
        category = template.translate_category(item['category'])
        if spider.name == 'hardwareinfo':
            temp = template.get_template(category)
            item = template.translate_item(temp, item)
            json_item = json.dumps(item)
            self.add(json_item, category)
        else:
            temp = template.get_template('record')
            item = template.translate_item(temp, item)
            json_item = json.dumps(item)
            self.add_item_to_list(json_item, category)

    def post_item(self, item, category):
        url = 'http://localhost:6543/category/{}/product/'.format(category)
        response = urllib2.Request(url, item)
        response.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(response)
        print resp
        return {
            "message": "item posted"
        }

    def post_price_list(self, item_list, category):
        url = 'http://localhost:6543/category/{}/record/'.format(category)
        # json_item_list = json.dumps([dict(item=item) for item in item_list])
        json_item = {}
        json_item['items'] = item_list
        response = urllib2.Request(url, json.dumps(json_item))
        response.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(response)
        print resp
        return {
            "message": "price posted"
        }

    def add_item_to_list(self, item, category):
        """ adding the items to a list. This is done so we dont have to
        send a request to the server for every item. But you can send one for
        every category. this reduces the server load"""
        self.items[self.category_list_mapping[category]].append(item)
        return

    def close_spider(self, spider):
        """ invalidate cache after mutation"""
        r = redis.StrictRedis(host=self.root_url, port=self.redis_port, db=0)
        category_keys = r.keys('categor*')  # both category and categories
        for key in category_keys:
            r.delete(key)

        for i in range(0, len(self.items)):
            self.post_price_list(self.items[i], self.category_names[i])
