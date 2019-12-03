# -*- coding: utf-8 -*-
"""Read the custom fields
"""
import sortly
from sortly.constants import *
import pandas as pd


def main():
    custom_fields_file_path = '/home/alxfed/archive/sortly_custom_fields.csv'
    per_page = 100
    page_num = 1
    response, rem = sortly.list.custom_fields(per_page, page_num)
    data = response['data']
    custom_fields = pd.DataFrame(data, dtype=object)
    # custom_fields['id'] = custom_fields['id'].astype(dtype=int)
    custom_fields['created_at'] = pd.to_datetime(custom_fields['created_at'])
    custom_fields['updated_at'] = pd.to_datetime(custom_fields['updated_at'])
    custom_fields.to_csv(custom_fields_file_path, index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')