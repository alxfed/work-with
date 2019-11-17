# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import numpy as np
import string
import odbc
import sqlalchemy as sqlalc


def main():
    name_of_dsn = 'center'
    '''
    connection_string = f'DSN={name_of_dsn}'
    connection = pyodbc.connect(connection_string, autocommit=True)
    SQL = 'select * from houzz'
    data = pd.read_sql(SQL, connection)
    '''
    connection = odbc.dbase.connection_with(name_of_dsn)
    SQL = 'select * from rand'
    data = pd.read_sql_query(SQL, connection)
    connection.close()

    other_conn = sqlalc.create_engine('sqlite:///home/alxfed/dbase/home.sqlite')
    other = pd.read_sql(SQL, con=other_conn)
    lett = list(string.ascii_lowercase)
    df = pd.DataFrame(np.random.choice(lett, size=(3, 3)), index=['a', 'b', 'c'], columns=[0, 1, 2])
    res = df.to_sql(name='rand', con=connection, if_exists='replace')
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')