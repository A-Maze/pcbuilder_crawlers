import HTMLParser
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

root_url = "http://nl.hardware.info/productgroep/{}/producten"
allowed_urls = (
    # "7/behuizingen",
    # "20/geheugenmodules",
    # "1/moederborden",
    "3/processors",
    # "21/voedingen",
    # "5/videokaarten",
    # "23/casefans",
    # "19/cpu-koelers",
    # "4/harddisksssds"
    # "2/optischedrives"
)

html = HTMLParser.HTMLParser()


class HardwareInfoSpider(CrawlSpider):
    name = "hardwareinfo"
    allowed_domains = ["http://nl.hardware.info",
                       "nl.hardware.info"]
    start_urls = (root_url.format(allowed_url) for allowed_url in allowed_urls)

    # Extract product specification links, follow them and extract the result
    # to the parse method
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='pagination']"),
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//table[@id='productresulttable']"
                                            ),
                           allow=("specificaties",)),
             follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        # The key is always the value of the second td  in the specifications
        # table. The value belonging to the key is the third td.
        key_xpath = "td[position()=2]/text()"
        value_xpath = "td[position()=3]/text()"

        # Append a before text() for values inside links
        link_value_xpath = re.sub(r'(text())', r'a/\1', value_xpath)

        # Hardware info uses an image with a tick that specifies if product has
        # something. The alt specifies this in text in the form of "ja" or
        # "nee"
        tick_value_path = "{}/{}".format(value_xpath.split('/', 1)[0],
                                         "img/@alt")

        product = {}
        product["category"] = html.unescape(''.join(response.xpath("//ul[@class='breadcrumb']\
            /li[3]/a/text()").extract()))

        # Get the specifications div
        for sel in response.xpath(
                "//*[@id='contentWithoutSidebar']/div/div[2]/div"):

            # Select the tables and loop trough the rows
            for row in sel.xpath("table/tbody/tr"):
                # Lookup the key and value and append them to the product
                key = html.unescape(''.join(row.xpath(key_xpath).extract()))
                value = html.unescape(''.join(row.xpath(value_xpath)
                                              .extract()).strip())

                link_value = html.unescape(''.join(row.xpath(link_value_xpath)
                                                   .extract()).strip())
                tick_value = html.unescape(''.join(row.xpath(tick_value_path)
                                                   .extract()).strip())

                # If the value is actually nested in a link or img use that
                # value
                if link_value:
                    value = link_value
                elif tick_value:
                    value = tick_value

                product[key] = value

        yield product
