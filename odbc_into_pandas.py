# -*- coding: utf-8 -*-
"""...
"""
import pyodbc as odbc
import pandas as pd


def main():
    connection_string = 'firstbase'
    connection = odbc.connect(connection_string, autocommit=True)
    SQL = 'select * from yelp'
    data = pd.read_sql(SQL, connection)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')