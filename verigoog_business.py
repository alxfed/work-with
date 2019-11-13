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

    addre = 'D CONSTRUCTION, INC' #''

    location = {'lat': 41.8781136, 'lng': -87.6297982}

    bias = 'circle:50000@' + str(location['lat']) + ',' + str(location['lng'])
    maps_client = googlemaps.Client(key=token, timeout=10,
                                    retry_timeout=2,
                                    queries_per_second=1,
                                    retry_over_query_limit=True)
    result = maps_client.find_place(input=addre,
                                    input_type="textquery",
                                    fields=['place_id', 'types'],
                                    location_bias=bias)
    if result['status'] == 'ZERO_RESULTS':
        print('None')
    elif result['status'] == 'OK':
        print('Some')
        candidates    = result['candidates']
    another_result = maps_client.places(query=addre,
                                        location=location,
                                        radius=50000,
                                        type='general_contractor')
    if another_result['status'] == 'OK':
        print('Some')
        place_id = another_result['results'][0]['place_id']
    candidates_list = []
    '''
    'place_id': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
    'plus_code': {'compound_code': '7P88+JW Coal City, Illinois', 'global_code': '86HH7P88+JW'}, 
    'rating': 3.5, 
    'reference': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
    'types': ['general_contractor', 'point_of_interest', 'establishment']
    '''
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