# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import pandas as pd
import sqlite3


def main():
    connection = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    sql = 'select * from companies'
    companies = pd.read_sql(sql=sql, con=connection)
    licensed_gen_contractors = pd.read_sql_table(table_name='licensed_general_contractors', con=connection)
    licensed_gen_contractors = licensed_gen_contractors.fillna('')
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')

