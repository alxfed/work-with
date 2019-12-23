# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc
import datetime as dt


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)

    data = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn_source)

    start_date  = dt.datetime(year=2019, month=12, day=1, hour=0, minute=0, second=0)
    end_date    = dt.datetime(year=2019, month=12, day=24, hour=0, minute=0, second=0)

    fresh_deals = data[(data['createdate'] > start_date) & (data['createdate'] < end_date)]

    if not fresh_deals.empty:
        fresh_deals.to_sql(
            name=sorting.FRESH_DEALS_TABLE,
            con=conn_target, if_exists='replace', index=False)
    else:
        print('No deals created in this time frame')
    return


if __name__ == '__main__':
    main()
    print('main - done')