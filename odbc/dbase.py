# -*- coding: utf-8 -*-
"""...
"""
import pyodbc
from . import constants


def connection_with(datasourcename):
    '''journal_mode=WAL if you need a concurrent reading
    by another process
    '''
    connection_string = f'DSN={datasourcename}'
    connection = pyodbc.connect(connection_string, autocommit=True)
    return connection
'''
    cursor.execute("SELECT ")
    for row in cursor.fetchall():
        print(row)
'''


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')