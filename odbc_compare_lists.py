# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import pandas as pd
from sqlalchemy.schema import MetaData

def main():
    connection = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    # sql = 'select * from companies'
    table_name = 'companies'
    meta = MetaData(connection)
    meta.reflect(only=[table_name], views=True)
    companies = pd.read_sql_table(table_name=table_name, con=connection)
    licensed_gen_contractors = pd.read_sql_table(table_name='licensed_general_contractors', con=connection)
    licensed_gen_contractors = licensed_gen_contractors.fillna('')
    print('ok')

    return


if __name__ == '__main__':
    main()
    print('main - done')

