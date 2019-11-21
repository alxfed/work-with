# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc


def main():
    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    data = pd.read_sql_table(table_name='companies', con=conn) # works
    id = data['companyId'][0]
    deleted = data['isDeleted'][0]
    name = data['name'][0]
    phone = data['phone'][0]
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')