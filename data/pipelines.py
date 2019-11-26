# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import odbc

class DataPipeline(object):

    database_name = 'data'
    table_name = 'scraped_data'

    def open_spider(self, spider):
        self.cnxn = odbc.dbase.connection_with(self.database_name)
        self.curs = self.cnxn.cursor()
        self.curs.execute('drop table if exists scraped_data')
        self.curs.execute('''create table ?(
                            one text,
                            two text,
                            three text''', self.table_name)

    def close_spider(self, spider):
        self.cnxn.close()

    def store(self, item):
        self.curs.execute("""insert into scraped_data values(?, ?, ?)""",
                              item['one'],
                              item['two'],
                              item['three'])

    def process_item(self, item, spider):
        self.store(item)
        print('Pipeline has stored an item to database')
        return item
