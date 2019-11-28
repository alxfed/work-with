# -*- coding: utf-8 -*-
import scrapy
from data.items import LicenseTableLine


class HeadlessReaderRobot(scrapy.Spider):

    name = 'basic_headless'

    def start_requests(self):
        url = 'https://webapps1.chicago.gov/activegcWeb/'
        for page_num in range(1, 16):
            cb_kwargs = {'page_num': page_num}
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, cb_kwargs=cb_kwargs )

    def parse(self, response, **cb_kwargs):
        # td/label/text()
        page_num = cb_kwargs['page_num']
        table_rows_xpath = '//table[contains(@class,"gridStyle-table")]/tbody/tr[contains(@class,"gridStyle-tr-alt-data")]'
        table_selector = response.xpath(table_rows_xpath)
        for table_line in table_selector:
            line = LicenseTableLine()
            line['lic_type']    = table_line.xpath('td[1]/label/text()').get()
            line['comp_name']   = table_line.xpath('td[2]/label/text()').get()
            line['address']     = table_line.xpath('td[3]/label/text()').get()
            line['phone']       = table_line.xpath('td[4]/label/text()').get()
            line['lic_expr']    = table_line.xpath('td[5]/label/text()').get()
            line['pins_expr']   = table_line.xpath('td[6]/label/text()').get()
            line['sins_expr']   = table_line.xpath('td[7]/label/text()').get()
            yield line
