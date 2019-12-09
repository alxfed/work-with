# -*- coding: utf-8 -*-
import scrapy
from data.items import LicenseTableLine


class HeadlessReaderRobot(scrapy.Spider):

    name = 'licensed_general_contractors'

    def start_requests(self):
        url = 'https://webapps1.chicago.gov/activegcWeb/'
        for page_num in range(1, 16):
            cb_kwargs = {'page_num': page_num}
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, cb_kwargs=cb_kwargs )

    def parse(self, response, **cb_kwargs):
        page_num = cb_kwargs['page_num']
        table_rows_xpath = '//table[contains(@class,"gridStyle-table")]/tbody/tr[contains(@class,"gridStyle-tr-alt-data")]'
        table_selector = response.xpath(table_rows_xpath)
        for table_line in table_selector:
            line = LicenseTableLine()
            line['license_type']    = table_line.xpath('td[1]/label/text()').get()
            line['company_name']   = table_line.xpath('td[2]/label/text()').get()
            line['street_address']     = table_line.xpath('td[3]/label[1]/text()').get().strip()
            line['city']        = table_line.xpath('td[3]/label[2]/text()').get().strip()
            line['state']       = table_line.xpath('td[3]/label[3]/text()').get().strip()
            line['zip']         = table_line.xpath('td[3]/label[4]/text()').get()
            line['phone']       = table_line.xpath('td[4]/label/text()').get().strip().replace(' x', '')
            line['license_expr']    = table_line.xpath('td[5]/label/text()').get()
            line['primary_insurance_expr']   = table_line.xpath('td[6]/label/text()').get()
            line['secondary_insurance_expr']   = table_line.xpath('td[7]/label/text()').get()
            yield line
