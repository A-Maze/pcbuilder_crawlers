from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

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

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//table[@id='productresulttable']"
                                            ),
                           allow=("specificaties",)),
             follow=True, callback='parse_item'),
    )
    print("test")

    def parse_item(self, response):
        key_xpath = "tr/td[@position=1]"
        value_xpath = "tr/td[@position=2]"
        for sel in response.xpath("//div[@id='columnleft']"):
            product = {}
            self.logging.info(sel)

            for row in sel.xpath("table/tbody/"):
                self.logging.info(row)
                product[row.xpath(key_xpath).extract()] = row.\
                    xpath(value_xpath).extract()
            yield product
