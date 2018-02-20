# -*- coding: utf-8 -*-
import scrapy


class GatherUrlsSpider(scrapy.Spider):
    name = 'gather_urls'
    start_urls = [
        'https://remixshop.com/bg'
    ]

    def parse(self, response):
        urls = response.css('.product-photos::attr(href)').extract()

        for url in urls:
            #     yield {'url':  response.urljoin(url)}
            with open('tmp/urls.txt', 'a') as f:
                f.write(response.urljoin(url))
                f.write("\n")

        # This is the part which crawls different pages
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)
