# -*- coding: utf-8 -*-
"""...
"""
import requests
from .constants import *

def list_of_items():
    sortly_rate_limit_max = 0
    sortly_rate_limit_remaining = 0
    sortly_rate_limit_reset = 0
    params = {'per_page': 10,
              'page': 1,
              # 'folder_id': 'null',
              'include': 'custom_attributes'}
    res = requests.get(url=ITEMS_URL, headers=authorization_header, params=params)
    headers = res.headers
    sortly_rate_limit_max = headers['Sortly-Rate-Limit-Max']
    sortly_rate_limit_remaining = headers['Sortly-Rate-Limit-Remaining']
    sortly_rate_limit_reset = headers['Sortly-Rate-Limit-Reset']
    resp = res.json()
    return resp, sortly_rate_limit_remaining


def custom_fields(per_page, page_num):
    params = {'per_page': per_page,
              'page': page_num}
    res = requests.get(url=LIST_CUSTOM_FIELDS_URL, headers=authorization_header, params=params)
    headers = res.headers
    # sortly_rate_limit_max = headers['Sortly-Rate-Limit-Max']
    remains = headers['Sortly-Rate-Limit-Remaining']
    # sortly_rate_limit_reset = headers['Sortly-Rate-Limit-Reset']
    resp = res.json()
    return resp, remains


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')