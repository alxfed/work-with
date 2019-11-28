# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LicenseTableLine(scrapy.Item):
    lic_type = scrapy.Field()
    comp_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()
    phone = scrapy.Field()
    lic_expr = scrapy.Field()
    pins_expr = scrapy.Field()
    sins_expr = scrapy.Field()