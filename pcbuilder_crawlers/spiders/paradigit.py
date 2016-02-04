import HTMLParser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

root_url = "http://www.paradigit.nl/componenten/{}"
allowed_urls = [
    "behuizingen",
    "geheuigen-intern",
    "moederborden",
    "processoren",
    "voedingen",
    "videokaarten",
    "koelers-en-koelpasta",
    "processor-koelers",
    "interne-harde-schijven",
    "solid-state-drives-ssd",
    "dvd-blu-ray-drives"
]

html = HTMLParser.HTMLParser()


class ParadigitSpider(CrawlSpider):
    name = "paradigit"
    allowed_domains = ["www.paradigit.nl"]

    start_urls = (root_url.format(allowed_url) for allowed_url in allowed_urls)

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//a[@class='PagerHyperlinkStyle']"),
            follow=True),
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class="
                          "'itemlistcombined-moreinfocontainer']/a"),
            follow=True, callback="parse_item")
        )

    def parse_item(self, response):
        manufacturer_number = (
            "//div[@class='itemdetail-specificationstab-mpncontainer']/{}")
        product_number = (
            "//div[@class='itemdetail-specificationstab-"
            "productnumbercontainer']/{}")
        key_xpath = "div[@position=1]/span/text()"
        value_xpath = "div[@position=2]/span/text()"

        rows = [manufacturer_number, product_number]
        product = {}
        product['price'] = html.unescape(response.xpath(
            "//meta[@itemprop='price']/text()").extract())
        product['category'] = html.unescape(response.xpath(
            "//div[@class='breadcrumb']/div[@position=2]/a/text()").extract())

        for row in rows:
            key = html.unescape(''.join(
                response.xpath(row.format(key_xpath)).extract()))
            value = html.unescape(''.join(
                response.xpath(row.format(value_xpath))
                .extract()).strip())
            product[key] = value
        yield product
