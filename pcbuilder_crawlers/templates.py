import json


class PcbuilderCrawlersTemplateInterface(object):
    def get_template(self, key):
            template = None
            return template

    def translate_category(name):
        with open('.templates/category.json') as data:
            categories = json.load(data)
        for category_names in categories:
            if name in category_names:
                return category_names[0]
        return None
