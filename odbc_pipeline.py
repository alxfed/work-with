# -*- coding: utf-8 -*-
"""...
"""
import pyodbc


class main(object):

    odbc_dsn = 'data'
    odbc_table = 'scrapy_result'

    def open_spider(self, spider):
        conn_string = f'DSN={self.odbc_dsn}'
        self.cnxn = pyodbc.connect(conn_string, autocommit=True)
        self.curs = self.cnxn.cursor()
        sql = """drop table if exists scrapy_result"""
        self.curs.execute(sql)
        self.curs.execute('''create table ?(one text, two text, three text)''', self.odbc_table)

    def close_spider(self, spider):
        self.cnxn.close()
        pass

    def store(self, item):
        self.curs.execute("""insert into scraped_data values(?, ?, ?)""",
                              item['one'],
                              item['two'],
                              item['three'])
        pass


if __name__ == '__main__':
    spider = ''
    main = main()
    main.open_spider(spider)
    print('main - done')