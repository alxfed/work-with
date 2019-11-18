# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
from numpy import nan
import sqlalchemy as sqlalc


def dateparse(x):
    if x is nan:
        return # datetime(2018, 12, 8, 0, 0)
    else:
        return pd.datetime.strptime(x, '%m/%d/%y') #  %H:%M:%S.%f if there are hours, minutes, seconts and milliseconds


def main():
    # all companies from HubSpot
    downuploaded_companies = '/home/alxfed/archive/companies_database.csv'

    request_params = ['name', 'phone', 'phone_mobile', 'phone_voip',
                      'phone_toll','phone_landline','phone_unidentified',
                      'address','city','zip','state', 'category','website']

    normal_columns = ['companyId', 'isDeleted', 'name', 'phone', 'phone_mobile',
                      'phone_voip', 'phone_toll', 'phone_landline',
                      'phone_unidentified', 'address', 'city', 'zip', 'state',
                      'category', 'website']

    all_companies_cdr, all_columns = hubspot.companies.get_all_companies_oauth(request_params)
    all_companies = pd.DataFrame(all_companies_cdr, columns=normal_columns)
    all_companies.fillna(value='', inplace=True)
    all_companies['companyId'] = all_companies['companyId'].astype(dtype=int)
    all_companies['isDeleted'] = all_companies['isDeleted'].astype(dtype=bool)
    all_companies['name'] = all_companies['name'].astype(dtype=object)
    all_companies['phone'] = all_companies['phone'].astype(dtype=object)
    all_companies['address'] = all_companies['address'].astype(dtype=object)
    all_companies['city'] = all_companies['city'].astype(dtype=object)
    all_companies['zip'] = all_companies['zip'].astype(dtype=object)
    all_companies['state'] = all_companies['state'].astype(dtype=object)
    all_companies['category'] = all_companies['category'].astype(dtype=object)
    all_companies['website'] = all_companies['website'].astype(dtype=object)

    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    all_companies.to_sql(name='companies', con=conn, if_exists='replace',
                         index=False)

    with open(downuploaded_companies, 'w') as f:
        f_csv = csv.DictWriter(f, normal_columns)
        f_csv.writeheader()
        f_csv.writerows(all_companies_cdr)
    return


if __name__ == '__main__':
    main()
    print('main - done')

'''
    gen_contractors = pd.read_csv(gen_cont_file_path,
                                  usecols=input_columns,
                                  parse_dates=['license_expr',
                                               'primary_insurance_expr',
                                               'secondary_insurance_expr'],
                                  date_parser=dateparse,
                                  dtype=object)
    all_rows = []
    for index, contractor in gen_contractors.iterrows():
        row = {}
        row['company_name'] = contractor['company_name']
        phone = contractor['phone'].replace('x', '')
        row['phone'] = phone
        street_address = ''; city = ''; state = ''; zip = ''
        addr = str(contractor['address'])
        if not (addr == ''):
            address = addr.replace('\xa0\xa0', '\xa0')
            street_address, sep, city_state_zip = address.partition('\xa0')
            city, sep, state_zip = city_state_zip.partition('\xa0')
            state, sep, zip = state_zip.partition('\xa0')
        row['street_address'] = street_address
        row['city'] = city
        row['state'] = state
        row['zip'] = zip
        row['license_type'] = contractor['license_type']
        row['license_expr'] = contractor['license_expr']
        row['primary_insurance_expr'] = contractor['primary_insurance_expr']
        row['secondary_insurance_expr'] = contractor['secondary_insurance_expr']
        all_rows.append(row)

    licensed_general_contractors = pd.DataFrame(all_rows)
    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    licensed_general_contractors.to_sql(name='licensed_general_contractors',
                                        con=conn, if_exists='replace', index=False)
'''