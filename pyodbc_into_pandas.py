# -*- coding: utf-8 -*-
"""...
"""
import pyodbc as odbc
import pandas as pd
import numpy as np
import string


def main():
    connection_string = 'DSN=center'
    connection = odbc.connect(connection_string, autocommit=True)
    '''
    SQL = 'select * from houzz'
    data = pd.read_sql(SQL, connection)
    '''
    lett = list(string.ascii_lowercase)
    df = pd.DataFrame(np.random.choice(lett, size=(3, 3)), index=['a', 'b', 'c'], columns=[0, 1, 2])
    res = df.to_sql(name='rand', con=connection)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')