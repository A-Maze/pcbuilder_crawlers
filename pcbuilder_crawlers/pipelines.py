from scrapy.settings import Settings
from template import TemplateInterface

config = Settings()


class Pipeline(object):

    def process_item(self, item, spider):
        template = TemplateInterface()
        category = template.translate_category(item['category'])
        temp = template.get_template(category)
        item = template.translate_item(temp, item)

    def post_item(self, item):
        return item

    def post_price(self, item):
        return item
