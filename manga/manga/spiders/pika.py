import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

from manga.items import MangaItem

class PikaSpider(CrawlSpider):
    name = "pika"
    allowed_domains = ["pika.fr"]
    start_urls = [
        "http://www.pika.fr/planning/2000/04"
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('ul.pagine li:not(.first) a'))),
        Rule(LinkExtractor(allow=(), restrict_css=('div.nav.fr span.next_page a'))),
        Rule(LinkExtractor(allow=(), restrict_css=('div.listing-bookV.listing-4.node .titre-book a')), callback='parse_item'),
    )

    def parse_item(self, response):
        item = MangaItem()
        item['name'] = response.css("h1.titre-big").xpath('./text()').extract()
        item['release_date'] = response.css("div.date_sortie").xpath('./text()').extract()
        item['collection'] = response.css("div.categorie").xpath('./text()').extract()
        item['cover'] = response.css("div.mediao__figure").xpath('./@data-popin').extract()
        item['tome'] = response.css("div.block_infos_techniques div:nth-child(2)").xpath('./text()').extract()
        yield item
