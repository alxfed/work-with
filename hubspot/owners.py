# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants

def get_owners():
    resp = requests.request("GET", url=constants.OWNERS_URL, headers=constants.authorization_header)
    response = resp.json()
    return response


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')