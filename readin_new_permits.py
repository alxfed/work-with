# -*- coding: utf-8 -*-
"""...
"""
import socradata
import pandas as pd
import datetime as dt


def main():
    dataset = 'ydr8-5enu'  # permits data
    column = 'issue_date'
    start_dt = dt.datetime(year=2019, month=11, day=1, hour=0, minute=0, second=0)
    start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
    end_dt = dt.datetime(year=2019, month=12, day=1, hour=0, minute=0, second=0)
    end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
    response = socradata.datasets.where_a_lot_between(dataset, column, start_str, end_str)
    result = pd.DataFrame.from_records(response)

    return


if __name__ == '__main__':
    main()
    print('main - done')