# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import numpy as np
import string
import pyodbc
import sqlalchemy as sqlalc


def main():
    datasourcename = 'data'
    conn_string = f'DSN={datasourcename}'
    # conn_string = '"Driver=SQLite3;Database=/home/alxfed/dbase/sqlite.db"'
    conn = pyodbc.connect(conn_string, autocommit=True, timeout=2000)
    curs = conn.cursor()
    table = 'test_table'
    curs.execute(f"""drop table if exists {table}""")
    sql = 'create table test_table (one text, two text, three text)'
    curs.execute(sql)
    sql = 'insert into test_table(one, two, three) values ("one", "two", "three")'
    curs.execute(sql)
    curs.commit()
    conn.close()
    return


if __name__ == '__main__':
    main()
    print('main - done')


# self.curs.execute('drop table if exists ?', self.odbc_table)
        # self.curs.execute('''create table ?(
        #                     one text,
        #                     two text,
        #                     three text''', self.odbc_table)