import scrapy

from manga.items import MangaItem

class PikaSpider(scrapy.Spider):
    name = "pika"
    allowed_domains = ["pika.fr"]
    start_urls = [
        "http://www.pika.fr/planning/2000/04"
    ]

    def parse(self, response):
        mangaSelectors = response.css("div.listing-bookV.listing-4.node div.item")
        for sel in mangaSelectors:
            item = MangaItem()
            item['name'] = sel.css("span.titre-book a").xpath('./text()').extract()
            item['release_date'] = sel.css("span.date_sortie").xpath('./text()').extract()
            item['collection'] = sel.css("span.categorie").xpath('./text()').extract()
            item['author'] = sel.css("span.author").xpath('./text()').extract()
            item['cover'] = sel.css("div.mediao__figure img").xpath('./@src').extract()
            yield item

        if len(mangaSelectors) == 0:
            return
        next_page = response.css("ul.pagine li:not(.first) a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

        next_month = response.css("div.nav.fr span.next_page a::attr('href')")
        if next_month:
            url = response.urljoin(next_month[0].extract())
            yield scrapy.Request(url, self.parse)
