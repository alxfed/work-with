# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
import sqlalchemy as sqlalc
import sorting


def main():
    # all companies from HubSpot
    downuploaded_contacts = '/home/alxfed/archive/contacts_database_all.csv'
    contact_properties_table_url = '/home/alxfed/archive/contact_properties_table.csv'

    request_params = []

    normal_columns = ['companyId', 'isDeleted', 'name', 'phone',
                      'address', 'city', 'zip', 'state',
                      'category','domain', 'website',
                      'summary_note_number', 'summary_note_date_str',
                      'elgoog_place_id', 'elgoog_types']

    contact_properties_columns = ['name', 'label', 'description']

    all_props_list = hubspot.contacts.get_all_contact_properties()
    all_props_table = []
    line = dict()
    for prop in all_props_list:
        name = prop['name']
        request_params.append(name)
        normal_columns.append(name)
        line['name'] = name
        line['label'] = prop['label']
        line['description'] = prop['description']
        all_props_table.append(line)

    contact_properties_table = pd.DataFrame(all_props_table, columns=contact_properties_columns)
    contact_properties_table.to_csv(contact_properties_table_url, index=False)

    all_contacts_cdr, all_columns = hubspot.contacts.get_all_contacts_oauth(request_params)
    all_contacts = pd.DataFrame(all_contacts_cdr, columns=all_columns)

    # formatting
    all_contacts.fillna(value='', inplace=True)
    all_contacts = all_contacts.astype(dtype=object)

    # store in home database
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_contacts.to_sql(
        name=sorting.constants.CONTACTS_EVERYTHING_TABLE, con=conn,
        if_exists='replace', index=False)

    # store in a file too
    with open(downuploaded_contacts, 'w') as f:
        f_csv = csv.DictWriter(f, all_columns)
        f_csv.writeheader()
        f_csv.writerows(all_contacts_cdr)

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
