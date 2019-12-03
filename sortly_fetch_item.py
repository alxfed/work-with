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
    item_id = '7140688'
    to_include = 'custom_attributes'
    response, rem = sortly.item.fetch(item_id, to_include)
    data = response['data']
    # item_list = pd.DataFrame(data, dtype=object)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')