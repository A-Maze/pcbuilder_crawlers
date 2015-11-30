import json


class TemplateInterface(object):
    def get_template(self, category):
        path = 'templates/{category}.json'.format(category=category)
        with open(path) as data:
            template = json.load(data) or None
        return template

    def translate_category(self, name):
        with open('templates/category.json') as data:
            categories = json.load(data)
        for category_names in categories:
            categoryArray = [i.encode('UTF-8') if isinstance(i, basestring)
                             else i for i in categories[category_names]]
            if name in categoryArray:
                return categoryArray[0]
        return None

    def translate_item(self, template, item):
        for row in item:
            for other_row in template:
                encoded_template_row = [i.encode('UTF-8')
                                        if isinstance(i, basestring)
                                        else i for i
                                        in template[other_row]]
                print other_row
                if row in encoded_template_row:
                    item[other_row] = item.pop(row)
        return item
