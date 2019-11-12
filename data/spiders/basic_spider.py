# -*- coding: utf-8 -*-
import scrapy


class BasicSpiderSpider(scrapy.Spider):
    name = 'basic_spider'
    allowed_domains = ['chicago.org']
    start_urls = ['http://chicago.org/']

    def parse(self, response):
        pass
