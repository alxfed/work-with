# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import odbc

class DataPipeline(object):

    table_name = 'scraped_data'

    def __init__(self, odbc_dsn):
        # while the instance of this pipeline is being created
        self.odbc_dsn = odbc_dsn

    @classmethod
    def from_crawler(cls, crawler):
        # before the instance of this pipeline is created.
        return cls(
            odbc_dsn = crawler.settings.get('ODBC_DSN')
        )

    def open_spider(self, spider):
        self.cnxn = odbc.dbase.connection_with(self.odbc_dsn)
        self.curs = self.cnxn.cursor()
        self.curs.execute('drop table if exists ?', self.table_name)
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
