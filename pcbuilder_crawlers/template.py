import json


class TemplateInterface(object):
    def get_template(self, category):
        path = 'templates/{category}.json'.format(category=category)
        with open(path, 'r') as data:
            template = json.load(data) or None
        return template

    def translate_category(self, name):
        with open('templates/category.json', 'rb') as data:
            categories = json.load(data)
        for category_names in categories:
            if name in categories[category_names]:
                return categories[category_names][0]
        return None

    def translate_item(self, template, item):
        """ this function checks for every row in the crawled item if the
            key exists in the template. If this is the case the key gets
            translated into English by adding a new key with the correct name
            and then removing the old one """
        for row in item:
            for template_row in template:
                if row in template[template_row]:
                    item[template_row] = item.pop(row)
        return item
