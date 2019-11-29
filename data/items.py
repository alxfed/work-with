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
    license_type = scrapy.Field()
    company_name = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip = scrapy.Field()
    phone = scrapy.Field()
    license_expr = scrapy.Field()
    primary_insurance_expr = scrapy.Field()
    secondary_insurance_expr = scrapy.Field()