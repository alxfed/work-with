# -*- coding: utf-8 -*-
"""...
"""
import googlemaps
import os
import time


def main():
    ELGOOG_TOKEN_FILE = '/home/alxfed/credo/elgoog_token.txt'
    token_file = open(ELGOOG_TOKEN_FILE, 'r')
    token = token_file.read()
    token_file.close()

    addre = 'ACRIS, INC.' #''

    location = {'lat': 41.8781136, 'lng': -87.6297982}

    bias = 'circle:50000@' + str(location['lat']) + ',' + str(location['lng'])
    maps_client = googlemaps.Client(key=token, timeout=10,
                                    retry_timeout=2,
                                    queries_per_second=1,
                                    retry_over_query_limit=True)
    result = maps_client.find_place(input=addre,
                                    input_type="textquery",
                                    fields=['place_id'],
                                    location_bias=bias)
    if result['status'] == 'ZERO_RESULTS':
        print('None')
    candidates    = result['candidates']
    candidates_list = []
    for candidate in candidates:
        place_id = candidate['place_id']
        contact = maps_client.place(place_id=place_id,
                                    fields=['name', 'formatted_address', 'formatted_phone_number', 'website'])
        res = contact['result']
        candidates_list.append(res)
        print('ok')

    print(result)
    return


if __name__ == '__main__':
    main()
    print('main - done')