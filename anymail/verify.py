# -*- coding: utf-8 -*-
"""...
"""
import requests
from .constants import *


def credits():
    # check the number of credits left
    r = requests.get(credits_check_url, headers=headers)
    if r.status_code == 200:
        resp = r.json()
        number = resp['credits_left']
        return number
    else:
        print('The API key is not working.', r.status_code)
        return


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')