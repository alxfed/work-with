# -*- coding: utf-8 -*-
"""...
"""
import pyodbc
from . import constants


def create_connection(datasourcename):
    '''journal_mode=WAL if you need a concurrent reading
    by another process
    '''
    connection = pyodbc.connect('DSN='+datasourcename, autocommit=True)
    cursor = connection.cursor()
    return cursor
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