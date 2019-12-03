# -*- coding: utf-8 -*-
"""...
"""
import requests
from .constants import *


def create_item():
    resp = requests.request(method='POST', headers=authorization_header)
    headers = resp.headers
    return


def fetch(item_id, *include):
    request_url = ITEMS_URL + f'/{item_id}'
    parameters = {}
    if include[0]:
        parameters = {'include': include[0]}  # TODO multiple parameters with comma
    res = requests.get(url=request_url, headers=authorization_header, params=parameters)
    rem = res.headers['Sortly-Rate-Limit-Remaining']
    item = res.json()
    return item, rem


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')