# -*- coding: utf-8 -*-
"""...
"""
import sorting
import sqlalchemy as sqlalc
import pandas as pd


def main():
    conn_source = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)
    verigoog = pd.read_sql_table(
        table_name=sorting.VERIGOOG_CONTRACTORS_TABLE, con=conn_source)

    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    licensed_gen_contractors = pd.read_sql_table(
        table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_reference)

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)

    companies['name'] = companies['name'].str.title()  # there are still some non-'title' names there

    # drop all the true duplicates
    verigoog = verigoog.drop_duplicates(subset='place_id', keep='first') # first is default, last can be set here
    # leave only the lines that contain general contractors
    verigoog = verigoog[verigoog['types'].str.contains('general_contractor')] # any position of the substring
    # format
    verigoog['name'] = verigoog['name'].str.title()

    conn_target = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)
    verigoog.to_sql(
        name=sorting.USABLE_VERIGOOGED_GENERAL,
        con=conn_target, if_exists='replace', index=False)

    merged = pd.merge(verigoog, companies, on=['name'], how='inner')
    merged.to_sql(
        name=sorting.INNER_MERGED_VERIGOOGED,
        con=conn_target, if_exists='replace', index=False)

    new_verigoog = pd.merge(verigoog, merged, on=['place_id'], how='outer')
    excluded_verigoog = new_verigoog[new_verigoog['companyId'].isnull()]
    excluded_verigoog = excluded_verigoog.drop(['formatted_address_y', 'formatted_phone_number_y',
           'name_y', 'types_y', 'companyId', 'isDeleted', 'phone',
           'address', 'city', 'zip', 'state', 'category', 'domain', 'website_x', 'website_y',
           'summary_note_number', 'summary_note_date_str'], axis=1)
    excluded_verigoog.rename(columns={'formatted_address_x': 'formatted_address',
                                      'formatted_phone_number_x': 'formatted_phone_number',
                                      'name_x':'name', 'place_id': 'place_id', 'types_x': 'types',
                                      'website':'website'}, inplace=True)
    excluded_verigoog.to_sql(
        name=sorting.USABLE_NEW_VERIGOOGED_GENERAL,
        con=conn_target, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('done')



    # verigoog = verigoog.set_index('name')
    # verigoog.sort_values(by=['name'], inplace=True)
    # first_unique_companies = verigoog.drop_duplicates(subset='name', keep='first')
    # first_unique_companies.sort_values(by=['name'], inplace=True)
