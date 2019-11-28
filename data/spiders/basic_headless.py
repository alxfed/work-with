# -*- coding: utf-8 -*-
import scrapy


class BasicSpiderSpider(scrapy.Spider):
    name = 'basic_headless'
    allowed_domains = ['chicago.gov']
    start_urls = ['https://webapps1.chicago.gov/activegcWeb/']

    def parse(self, response):
        pass
