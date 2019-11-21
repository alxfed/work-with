# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import numpy as np
import string
import odbc
import sqlalchemy as sqlalc


def main():
    name_of_dsn = 'home'

    connection = odbc.dbase.connection_with(name_of_dsn)
    SQL = 'select * from companies'
    data = pd.read_sql_query(SQL, connection)
    id = data['companyId'][0]
    deleted = data['isDeleted'][0]
    name = data['name'][0]
    phone = data['phone'][0]
    connection.close()
    return


if __name__ == '__main__':
    main()
    print('main - done')