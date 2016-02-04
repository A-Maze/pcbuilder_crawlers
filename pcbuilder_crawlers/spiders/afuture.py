import HTMLParser
import scrapy
from scrapy.spiders import Spider


root_url = "https://www.afuture.nl/productlist.php?categoryID={}"
allowed_urls = {
    "237": "case",
    "911": "memory",
    "164": "motherboard",
    "989": "cpu",
    "170": "video_card",
    "921": "cooler",
    "219": "hard_drive",
    "1563": "hard_drive",
    "214": "optical_drive"
}

html = HTMLParser.HTMLParser()


class AfutureSpider(Spider):
    name = "afuture"
    allowed_domains = ["https://www.afuture.nl",
                       "afuture.nl"]
    start_urls = (root_url.format(allowed_url) for allowed_url, value in
                  allowed_urls.items())

    def parse(self, response):
        """
        Retrieves the number of pages for each category and requests every
        page. Parses the response to the parse_page method
        """

        # selects the available amount of pages
        num_pages = int(response.xpath(
            "//*[@id='product-overzicht-nav']/li[9]/span/text()").extract()[0]
            .partition('t/m ')[-1].rpartition(' (')[0])
        category_id = response.url.split('=')[1]
        base_url = ("https://www.afuture.nl/ajax/"
                    "productlistAJAX.php?categoryID={}&".format(
                        category_id
                    ))
        # loop through all available pages of the category and parse them to
        # parse_page
        for page in range(1, num_pages):
            url = "{}currentIndex={}".format(base_url, page)
            print url
            yield scrapy.Request(url, dont_filter=True,
                                 callback=self.parse_page)

    def parse_page(self, response):
        """
        Retrieves the URL for the detail page of every product on the page
        sends a GET request to this URL. It then parses the response and
        the category to the parse_item method
        """

        # Get the current category based on the category ID in the URL
        category = allowed_urls[
            response.url.partition('=')[-1].rpartition('&')[0]
        ]

        # exctract the product table and parse every product to parse_item
        for product in response.xpath("//*[@id='producten-overzicht']/tbody"):
            yield scrapy.Request(
                "https://www.afuture.nl/{}".format(product.xpath(
                    "//td/a/@href"
                ).extract()[0]),
                dont_filter=True,
                callback=self.parse_item,
                meta={'category': category})

    def parse_item(self, response):
        """
        Scrapes the necesarry info of the product detail page and saves
        it in a dictionary
        """
        # The key is alway the th and value is always the td in the
        # information table
        key_xpath = "th/text()"
        value_xpath = "td/text()"

        product = {}
        product["category"] = response.meta['category']
        product["link"] = response.url
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
