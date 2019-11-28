# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import odbc

class DataPipeline(object):

    def __init__(self, odbc_dsn, odbc_table):
        # while the instance of this pipeline is being created
        self.odbc_dsn = odbc_dsn
        self.odbc_table = odbc_table

    @classmethod
    def from_crawler(cls, crawler):
        # before the instance of this pipeline is created.
        return cls(
            odbc_dsn = crawler.settings.get('ODBC_DSN'),
            odbc_table = crawler.settings.get('ODBC_TABLE')
        )

    def open_spider(self, spider):
        self.cnxn = odbc.dbase.connection_with(self.odbc_dsn)
        self.curs = self.cnxn.cursor()
        # self.curs.execute('drop table if exists ?', self.odbc_table)
        # self.curs.execute('''create table ?(
        #                     one text,
        #                     two text,
        #                     three text''', self.odbc_table)
        pass

    def close_spider(self, spider):
        self.cnxn.close()
        pass

    def store(self, item):
        # self.curs.execute("""insert into scraped_data values(?, ?, ?)""",
        #                       item['one'],
        #                       item['two'],
        #                       item['three'])
        pass

    def process_item(self, item, spider):
        self.store(item)
        print('Pipeline has stored an item to database')
        return item
