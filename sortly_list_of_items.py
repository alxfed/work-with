# -*- coding: utf-8 -*-
"""Read the custom fields
"""
import sortly
from sortly.constants import *
import pandas as pd


def main():
    # https://api.sortly.co/api/v1/items?per_page=2&page=1&folder_id=1&include=custom_attributes
    page_size = 10
    start_page = 1
    folder_id = 0
    response, rem = sortly.list.list_of_items()
    data = response['data']
    item_list = pd.DataFrame(data, dtype=object)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')