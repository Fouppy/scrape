import scrapy

from manga.items import MangaItem

class PikaSpider(scrapy.Spider):
    name = "pika"
    allowed_domains = ["pika.fr"]
    start_urls = [
        "http://www.pika.fr/planning/"
    ]

    def parse(self, response):
        for sel in response.css("div.listing-bookV.listing-4.node div.item"):
            item = MangaItem()
            item['name'] = sel.css("span.titre-book a").xpath('./text()').extract()
            item['date'] = sel.css("span.date_sortie").xpath('./text()').extract()
            item['collection'] = sel.css("span.categorie").xpath('./text()').extract()
            item['author'] = sel.css("span.author").xpath('./text()').extract()
            yield item

        next_page = response.css("ul.pagine li:not(.first) a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

        next_month = response.css("div.nav.fr span.next_page a::attr('href')")
        if next_month:
            url = response.urljoin(next_month[0].extract())
            yield scrapy.Request(url, self.parse)
