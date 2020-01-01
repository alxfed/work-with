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

    # verigoog = verigoog.set_index('name')
    # verigoog.sort_values(by=['name'], inplace=True)
    verigoog['name'] = verigoog['name'].str.title()
    verigoog = verigoog.drop_duplicates(subset='place_id', keep='first') # first is default, last can be set here
    # starts_with_gen_contractors = verigoog[verigoog['types'].str.startswith('general_contractor')]
    gen_contractor = verigoog[verigoog['types'].str.contains('general_contractor')] # any position of the substring
    first_unique_companies = verigoog.drop_duplicates(subset='name', keep='first')
    first_unique_companies.sort_values(by=['name'], inplace=True)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('done')