# -*- coding: utf-8 -*-
"""...
"""
import requests

ELGOOG_TOKEN_FILE = '/home/alxfed/credo/elgoog_token.txt'

chicago_location = {'lat': 41.8781136, 'lng': -87.6297982}
chicago_bias = 'circle:50000@' + str(chicago_location['lat']) + ',' + str(chicago_location['lng'])


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')