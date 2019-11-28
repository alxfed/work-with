import pyodbc


datasourcename = 'data'
conn_string = f'DSN={datasourcename}'
cnxn = pyodbc.connect(conn_string, autocommit=True)
# cnxn = pyodbc.connect('DRIVER={SQLite3};DATABASE=/home/alxfed/dbase/firstbase.sqlite')
cursor = cnxn.cursor()

cursor.execute("SELECT WORK_ORDER.TYPE,WORK_ORDER.STATUS, WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID FROM WORK_ORDER")
for row in cursor.fetchall():
    print(row)

def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')