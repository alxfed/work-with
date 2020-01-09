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
    elif r.status_code == 503:
        print('Anymailfind server is overloaded. 503')
        exit(246)
    else:
        print('The API key is not working.', r.status_code)
        exit(247)
    return


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')