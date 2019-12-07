# -*- coding: utf-8 -*-
"""Read the custom fields
"""
import sortly
from sortly.constants import *
import pandas as pd


def main():
    # https://api.sortly.co/api/v1/items/item_id?include=custom_attributes%2Cphotos
    # production jobs 7713864
    # toughy 7140688
    # south mount 7140690
    # test folder 8945363
    properties = {'name': 'API test folder',
                  'parent_id': None,
                  'type': 'folder'}

    response, rem = sortly.item.create(properties)
    data = response['data']
    # item_list = pd.DataFrame(data, dtype=object)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')