from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

root_url = "http://nl.hardware.info/productgroep/{}/producten"
allowed_urls = (
    "7/behuizingen",
    "20/geheugenmodules",
    "1/moederborden",
    "3/processors",
    "21/voedingen",
    "5/videokaarten",
    "23/casefans",
    "19/cpu-koelers",
    "4/harddisksssds",
    "2/optischedrives"
)


class HardwareInfoSpider(CrawlSpider):
    name = "hardwareinfo"
    allowed_domains = ["http://nl.hardware.info",
                       "nl.hardware.info"]
    start_urls = (root_url.format(allowed_url) for allowed_url in allowed_urls)

    # Extract product specification links, follow them and extract the result
    # to the parse method
    rules = (
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

        # Get the specifications div
        for sel in response.xpath(
                "//*[@id='contentWithoutSidebar']/div/div[2]/div"):
            product = {}

            # Select the tables and loop trough the rows
            for row in sel.xpath("table/tbody/tr"):
                # Lookup the key and value and append them to the product
                product[''.join(row.xpath(key_xpath).extract())] = \
                    ''.join(row.xpath(value_xpath).extract())
            yield product
