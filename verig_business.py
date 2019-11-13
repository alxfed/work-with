# -*- coding: utf-8 -*-
"""...
"""
import verigoog


def main():
    compa = 'D CONSTRUCTION, INC'  # name of the compan or another text string
    # text search with the help of find_place and bias, then place details for every candidate
    result = verigoog.places.find_in_chicago(compa)
    # search with text query, within a radius from a location with given type filtering
    other_result = verigoog.places.of_type_in_chicago(compa, 'general_contractor')
    print(result, '\n', other_result)
    return


if __name__ == '__main__':
    main()
    print('main - done')


'''
'place_id': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'plus_code': {'compound_code': '7P88+JW Coal City, Illinois', 'global_code': '86HH7P88+JW'}, 
'rating': 3.5, 
'reference': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'types': ['general_contractor', 'point_of_interest', 'establishment']
'''