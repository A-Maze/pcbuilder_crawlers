import json
import os

class TemplateInterface(object):
    def get_template(key):
            template = None
            return template

    def translate_category(self, name):
        with open('/home/rik/Project/A-Pc/pcbuilder_crawlers/pcbuilder_crawlers/templates/category.json') as data:
            categories = json.load(data)
        for category_names in categories:
            categoryArray = [i.encode('UTF-8') if isinstance(i, basestring)
                             else i for i in categories[category_names]]
            if name in categoryArray:
                print 'found'
                return categoryArray[0]
        return None
