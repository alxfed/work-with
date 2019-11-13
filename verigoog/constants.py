# -*- coding: utf-8 -*-
"""https://googlemaps.github.io/google-maps-services-python/docs/index.html#googlemaps.Client.find_place
"""
import requests

ELGOOG_TOKEN_FILE = '/home/alxfed/credo/elgoog_token.txt'

chicago_location = {'lat': 41.8781136, 'lng': -87.6297982}
chicago_bias = 'circle:50000@' + str(chicago_location['lat']) + ',' + str(chicago_location['lng'])

STATUS_CODES = [# 'OK', # indicates that no errors occurred; the place was successfully detected and at least one result was returned.
                'ZERO_RESULTS', # indicates that the search was successful but returned no results. This may occur if the search was passed a latlng in a remote location
                'OVER_QUERY_LIMIT', # indicates that you are over your quota.
                'REQUEST_DENIED', # indicates that your request was denied, generally because of lack of an invalid key parameter.
                'INVALID_REQUEST' # generally indicates that a required query parameter (location or radius) is missing.
                'UNKNOWN_ERROR']


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')