# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import pandas as pd
import sorting


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_companies = pd.read_sql_table(table_name=sorting.COMPANIES_TABLE, con=conn_reference)
    all_companies['companyId'] = all_companies['companyId'].astype(dtype=object)
    companyId = '2536529847'
    column = all_companies['companyId']
    print('Type: ', column.dtype)
    co_info = all_companies[all_companies['companyId'] == int(companyId)]
    print('ok', co_info)
    return


if __name__ == '__main__':
    main()
    print('main - done')