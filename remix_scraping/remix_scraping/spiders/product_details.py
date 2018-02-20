# -*- coding: utf-8 -*-
import scrapy

from remix_scraping.items import RemixScrapingItem


class ProductDetailsSpider(scrapy.Spider):
    name = 'product_details'
    f = open("tmp/urls.txt")
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    custom_settings = {
        'FEED_URI': 'tmp/product_details.csv'
    }

    def parse(self, response):
        single_item = RemixScrapingItem()
        single_item['title'] = response.css('.pr-title').extract_first().strip()
        single_item['price'] = response.css('.product-price::text').extract_first().strip()
        if single_item['price'] == "":
            single_item['price'] = response.css('.new-price::text').extract_first().strip()
        single_item['price'] = single_item['price'].replace(",", ".")
        single_item['size'] = response.css('.product-size::text')[1].extract().strip()
        single_item['description'] = response.css('.product-description::text')[1].extract().strip()

        yield single_item

