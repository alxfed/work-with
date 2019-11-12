# -*- coding: utf-8 -*-
"""...
"""
from .constants import *
import requests


def where_between(dataset, parameter, first_value, second_value):
    api_url = f'https://{CHICAGO_RESOURCE_URL}/resource/{dataset}.json'
    api_uri = api_url + f'?$where={parameter} between "{first_value}" and "{second_value}"'
    response = requests.request("GET", url=api_uri, headers=socrata_authorization_header)
    if response.status_code == 200:
        return response.json()
    else:
        return


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')