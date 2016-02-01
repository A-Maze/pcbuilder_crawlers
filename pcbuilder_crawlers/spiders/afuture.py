import HTMLParser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


root_url = "https://www.afuture.nl/productlist.php?categoryID={}"
allowed_urls = [
    "237",  # cases
    "911",  # memory
    "164",  # motherboard
    "989",  # CPU
    "170",  # GPU
    "921",  # fans
    "219"  # HDD
    "1563",  # SSD
    "214"  # optical drive
]

html = HTMLParser.HTMLParser()


class AfutureSpider(CrawlSpider):
    name = "afuture"
    allowed_domains = ["https://www.afuture.nl",
                       "afuture.nl"]
    start_urls = (root_url.format(allowed_url) for allowed_url in allowed_urls)

    # Extract product specification links, follow them and extract the result
    # to the parse method
    rules = (
        # 21 is the id for the next page link.
        Rule(LinkExtractor(restrict_xpaths="//*[@id='21']"), follow=True,
             callback="get_category"),
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
        product["category"] = html.unescape(self.category)
        product["price"] = html.unescape("".join(response.xpath(
            "//*[@id='product-detail-prijs-incl']/text()").extract()[0]).split()[1])  # noqa
        product["webshop"] = 'afuture'

        for table in response.xpath("//table[@id='product-detail-informatie']"):  # noqa
            for row in table.xpath("tr"):
                key = html.unescape(''.join(row.xpath(key_xpath).extract()))
                value = html.unescape(''.join(row.xpath(value_xpath)
                                              .extract()).strip())

                product[key] = value

        yield product

    def get_category(self, response):
        self.category = "".join(response.xpath("//*[@id='content']/h1/text()").extract()).strip()  # noqa
        print self.category
