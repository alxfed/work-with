# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.SOURCE_DATABASE_URI)
    data = pd.read_sql_table(table_name=sorting.NEW_PERMITS_TABLE, con=conn_source)
    gen_contractors = pd.read_sql_table(table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_source)
    companies = pd.read_sql_table(table_name=sorting.COMPANIES_TABLE, con=conn_source)
    companies_list = companies['name'].values
    # upload to the next stage database
    result = pd.DataFrame()
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    result.to_sql(name=sorting.NEW_COMPANIES_TABLE, con=conn_target, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')