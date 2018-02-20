# -*- coding: utf-8 -*-
import scrapy

from remix_scraping.items import RemixScrapingItem


class ProductSpiderSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = [
        'https://remixshop.com/bg'
    ]

    def parse(self, response):
        titles = response.css('.product-brand::text').extract()
        prices = response.css('.product-price::text').extract()
        new_prices = response.css('.new-price::text').extract()
        sizes = response.css('.product-size::text').extract()
        images = response.css('img::attr(data-img)').extract()

        for item in zip(titles, prices, new_prices, sizes, images):
            single_item = RemixScrapingItem()
            single_item['title'] = item[0].strip()
            single_item['price'] = item[1].strip()
            if item[1].strip() == "":
                single_item['price'] = item[2].strip()
            single_item['price'] = single_item['price'].replace(",", ".")
            single_item['size'] = item[3].strip()
            single_item['image_urls'] = [item[4]]
            yield single_item

        # This is the part which crawls different pages
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)