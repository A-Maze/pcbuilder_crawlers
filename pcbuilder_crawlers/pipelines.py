from spiders.hardware_info import HardwareInfoSpider
from scrapy.settings import Settings
from template import TemplateInterface

config = Settings()


class Pipeline(object):
    def __init__(self):
        self.root_url = config.get("API_URL")
        # self.api_url = ("{root_url}category/{category_name}/product"
        #                 "/{product_id}" .format(root_url=self.root_url))

    def process_item(self, item, spider):
        template = TemplateInterface()
        category = template.translate_category(item['category'])
        if spider is HardwareInfoSpider:
            self.post_item(item)
        else:
            self.post_price(item)
        return item

    def post_item(self, item):
        return item

    def post_price(self, item):
        return item
