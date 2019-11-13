# -*- coding: utf-8 -*-
"""...
"""
import verigoog
from .constants import *


def find_in_chicago(name_of_the_place):
    candidates_list = []
    result = verigoog.Client.find_place(input=name_of_the_place,
                                        input_type="textquery",
                                        fields=['place_id', 'types'],
                                        location_bias=chicago_bias)
    if result['status'] == 'ZERO_RESULTS':
        # print('None')
        return
    elif result['status'] == 'OK':
        # print('Some')
        pass
    candidates = result['candidates']
    for candidate in candidates:
        place_id = candidate['place_id']
        contact = verigoog.Client.place(place_id=place_id,
                                    fields=['place_id', 'name', 'type', 'formatted_address',
                                            'formatted_phone_number', 'website'])
        res = contact['result']
        candidates_list.append(res)
    return candidates_list


def of_type_in_chicago(name_of_the_place, type_string):
    candidates_list = []
    result = verigoog.Client.places(query=name_of_the_place,
                                    location=chicago_location,
                                    radius=50000,
                                    type=type_string)
    if result['status'] == 'ZERO_RESULTS':
        # print('None')
        return
    elif result['status'] == 'OK':
        # print('Some')
        pass
    candidates = result['results']
    for candidate in candidates:
        place_id = candidate['place_id']
        contact = verigoog.Client.place(place_id=place_id,
                                    fields=['place_id', 'name', 'type', 'formatted_address',
                                            'formatted_phone_number', 'website'])
        res = contact['result']
        candidates_list.append(res)
    return candidates_list


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')