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
    downuploaded_companies = '/home/alxfed/archive/companies_database.csv'
    company_properties_table_url = '/home/alxfed/archive/company_properties_table.csv'

    request_params = []

    normal_columns = ['companyId', 'isDeleted', 'name', 'phone',
                      'address', 'city', 'zip', 'state',
                      'category','domain', 'website',
                      'summary_note_number', 'summary_note_date_str',
                      'elgoog_place_id', 'elgoog_types']

    company_properties_columns = ['name', 'label', 'description']
    include_associations = True

    all_props_json = hubspot.companies.get_all_company_properties()
    all_props_table = []
    line = dict()
    for prop in all_props_json:
        name = prop['name']
        request_params.append(name)
        normal_columns.append(name)
        line['name'] = name
        line['label'] = prop['label']
        line['description'] = prop['description']
        all_props_table.append(line)

    company_properties_table = pd.DataFrame(all_props_table, columns=company_properties_columns)
    company_properties_table.to_csv(company_properties_table_url, index=False)

    all_companies_cdr, all_columns = hubspot.companies.get_all_companies_oauth(request_params)
    all_companies = pd.DataFrame(all_companies_cdr, columns=all_columns)
    # formatting
    all_companies.fillna(value='', inplace=True)
    all_companies = all_companies.astype(dtype=object)
    # store in home database
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_companies.to_sql(
        name=sorting.constants.COMPANIES_EVERYTHING_TABLE, con=conn,
        if_exists='replace', index=False)
    # store in a file too
    with open(downuploaded_companies, 'w') as f:
        f_csv = csv.DictWriter(f, all_columns)
        f_csv.writeheader()
        f_csv.writerows(all_companies_cdr)
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
