# -*- coding: utf-8 -*-
"""...
"""
import pyodbc
from . import constants


def create_connection_and_cursor():
    connection = pyodbc.connect('DRIVER={' + constants.DRIVER + '};DATABASE=' + constants.DRIVER)
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