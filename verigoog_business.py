# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import verigoog
import sorting
import pandas as pd


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_target = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)

    licensed_gen_contractors = pd.read_sql_table(
        table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_reference)

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)

    collected = pd.DataFrame()

    begin = 51; end = 100

    for index, contractor in licensed_gen_contractors.iterrows():
        if (index >= begin) and (index <= end):
            name = contractor['company_name']
            # companyId = contractor['Company ID']
            # text search with the help of find_place and bias, then place details for every candidate
            # result = verigoog.places.find_in_chicago(name)
            # search with text query, within a radius from a location with given type filtering
            result = verigoog.places.of_type_in_chicago(name, 'general_contractor')
            '''
            {'formatted_address': '2000 W 43rd St, Chicago, IL 60609, USA', 
            'formatted_phone_number': '(773) 735-0401', 
            'name': 'Seven D Construction', 
            'place_id': 'ChIJc858BlcsDogRb9D0nGelw58', 
            'types': ['general_contractor', 'point_of_interest', 'establishment'], 
            'website': 'http://www.7dconstruction.com/'}
            '''
            chunk = pd.DataFrame(result)
            if not chunk.empty:
                chunk = chunk.astype(dtype=object)
                chunk.to_sql(name=sorting.VERIGOOG_CONTRACTORS_TABLE,
                             con=conn_target, if_exists='append', index=False)
                print('Added candidates of ', index)

    # collected.to_sql(name=sorting.VERIGOOG_CONTRACTORS_TABLE,
    #                  con=conn_target, if_exists='append', index=False)
    print('Looks like it worked!')
    return


if __name__ == '__main__':
    main()
    print('Done')


'''
'place_id': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'plus_code': {'compound_code': '7P88+JW Coal City, Illinois', 'global_code': '86HH7P88+JW'}, 
'rating': 3.5, 
'reference': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'types': ['general_contractor', 'point_of_interest', 'establishment']
'''