# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
import sqlalchemy as sqlalc
import sorting


def main():
    # all contacts with all parameters from HubSpot
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    contact_properties_table_url = '/home/alxfed/archive/contact_properties_table.csv'

    request_params = []
    all_columns = ['vid', 'is_contact']

    contact_properties_columns = ['name', 'label', 'description']

    all_props_list = hubspot.contacts.get_all_contact_properties()
    contact_properties_df = pd.DataFrame(all_props_list,
                                            columns=contact_properties_columns)
    contact_properties_df.to_csv(contact_properties_table_url, index=False)

    request_params = contact_properties_df['name'].to_list()
    all_columns.extend(request_params)

    # pagination
    has_more = True
    offset = 0
    count = 100  # max 100

    # Now the main cycle
    while has_more:
        all_contacts_cdr, offset, has_more = hubspot.contacts.get_all_contacts_chunk(offset, request_params)
        all_contacts = pd.DataFrame(all_contacts_cdr, columns=all_columns)

        # formatting
        all_contacts.fillna(value='', inplace=True)
        all_contacts = all_contacts.astype(dtype=object)

        # store in home database
        all_contacts.to_sql(
            name=sorting.constants.CONTACTS_EVERYTHING_TABLE, con=conn,
            if_exists='append', index=False)

    return


if __name__ == '__main__':
    main()
    print('done')

'''

def getPandasSchema(df):
    takes a pandas dataframe and returns the dtype dictionary
    useful for applying types when reloading that dataframe from csv etc
    
    return dict(zip(df.columns.tolist(),df.dtypes.tolist()))
'''
