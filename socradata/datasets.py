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


def where_a_lot_between(dataset, parameter, first_value, second_value):
    def data_chunk(uri):
        response = requests.get(uri, headers=socrata_authorization_header)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            raise RuntimeError("Request Processing")
        elif response.status_code == 400:
            raise RuntimeError("Bad Request")
        elif response.status_code == 401:
            raise RuntimeError("Unauthorized")
        elif response.status_code == 403:
            raise RuntimeError("Forbidden")
        elif response.status_code == 404:
            raise RuntimeError("Not Found")
        elif response.status_code == 429:
            raise RuntimeError("Too many Requests")
        elif response.status_code == 500:
            raise RuntimeError("Server Error")
        else:
            return None  # silently return nothing

    api_url = f'https://{CHICAGO_RESOURCE_URL}/resource/{dataset}.json'
    api_call = api_url + f'?$where={parameter} between "{first_value}" and "{second_value}"'

    limit = 1000  # limit of the frame within the time window
    offset = 0
    data = []
    data_to_read_left = True

    while data_to_read_left:
        api_frame = api_call + f'&$limit={limit}&$offset={offset}'
        new_chunk = data_chunk(api_frame)
        data.extend(new_chunk)
        length = len(new_chunk)
        if length == limit:
            offset += limit
            print('offset: ', offset)
        else:
            data_to_read_left = False
    return data


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')