# -*- coding: utf-8 -*-
"""...
"""
import requests
from .constants import *

def custom_fields():
    res = requests.request(method='GET',
                           url=LIST_CUSTOM_FIELDS_URL,
                           headers=authorization_header)
    hdrs = res.headers
    resp = res.json()
    return resp, hdrs

def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')