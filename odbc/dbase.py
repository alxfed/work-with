# -*- coding: utf-8 -*-
"""...
"""
import pyodbc

DB_PATH = '/home/alxfed/dbase/firstbase.sqlite'
DRIVER = 'SQLite3'

connection = pyodbc.connect('DRIVER={' + DRIVER + '};DATABASE=' + DB_PATH)
cursor = connection.cursor()

cursor.execute("SELECT ")
for row in cursor.fetchall():
    print(row)


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')