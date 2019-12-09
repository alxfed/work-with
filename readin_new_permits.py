# -*- coding: utf-8 -*-
"""...
"""
import socradata
import pandas as pd
import datetime as dt
import sqlalchemy as sqlalc
import sorting


def main():
    dataset = 'ydr8-5enu'  # permits data
    column = 'issue_date'
    exclude_columns = ['location'] # 'xcoordinate, ycoordinate, latitude, longitude,
    start_dt = dt.datetime(year=2019, month=11, day=1, hour=0, minute=0, second=0)
    start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
    end_dt = dt.datetime(year=2019, month=12, day=1, hour=0, minute=0, second=0)
    end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
    response = socradata.datasets.where_a_lot_between(dataset, column, start_str, end_str)
    result = pd.DataFrame.from_records(response, exclude=exclude_columns)
    result['application_start_date'] = pd.to_datetime(result['application_start_date'], errors='coerce')
    result['issue_date'] = pd.to_datetime(result['issue_date'], errors='coerce')
    result['reported_cost'] = pd.to_numeric(result['reported_cost'], errors='coerce')
    result['xcoordinate'] = pd.to_numeric(result['xcoordinate'])
    result['ycoordinate'] = pd.to_numeric(result['ycoordinate'])
    result['latitude'] = pd.to_numeric(result['latitude'])
    result['longitude'] = pd.to_numeric(result['longitude'])

    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    result.to_sql(name='new_permits', con=conn, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')