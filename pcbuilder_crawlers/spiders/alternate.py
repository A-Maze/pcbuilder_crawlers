import HTMLParser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


root_url = "productlist.php?categoryID={}"
allowed = [
    "237",  # cases
    "911",  # memory
    "164",  # motherboard
    "989",  # CPU
    "170",  # GPU
    "921",  # fans
    "219",  # HDD
    "1563",  # SSD
    "214"  # optical drive
]

html = HTMLParser.HTMLParser()


class AlternateSpider(CrawlSpider):
    name = "alternate"
    allowed_domains = ["https://www.afuture.nl",
                       "afuture.nl"]
    start_urls = ("https://www.afuture.nl/",)
    allowed_urls = (root_url.format(allowed_url) for allowed_url in allowed)
    print allowed_urls

    # Extract product specification links, follow them and extract the result
    # to the parse method
    rules = (
        # third list position is components link list
        Rule(LinkExtractor(restrict_xpaths="//*[@id='mainnav']/li[3]",
             allow=allowed_urls), follow=True, callback="get_category"),

        # 21 is the id for the next page link.
        Rule(LinkExtractor(restrict_xpaths="//*[@id='21']"), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//a[@class='product-overzicht-item-fabrikant']"),
            follow=True, callback="parse_item")
    )

    def parse_item(self, response):
        # The key is alway the th and value is always the td in the
        # information table
        key_xpath = "th/text()"
        value_xpath = "td/text()"

        product = {}
        product["category"] = self.category
        product["price"] = response.xpath(
            "//*[@id='product-detail-prijs-incl']/text()").extract()

        for table in response.xpath("//div[@id='product-detail-informatie']"):

            for row in table.xpath("table/tbody/tr"):

                key = html.unescape(''.join(row.xpath(key_xpath).extract()))
                value = html.unescape(''.join(row.xpath(value_xpath)
                                              .extract()).strip())

                product[key] = value

        print product["category"]
        yield product

    def get_category(self, response):
        self.category = response.xpath("//*[@id='content']/h1/text()")\
            .extract()
