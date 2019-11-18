# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import csv
from numpy import nan
import sqlalchemy as sqlalc


def dateparse(x):
    if x is nan:
        return # datetime(2018, 12, 8, 0, 0)
    else:
        return pd.datetime.strptime(x, '%m/%d/%y') #  %H:%M:%S.%f if there are hours, minutes, seconts and milliseconds


def main():
    # active General Contractors are on https://webapps1.chicago.gov/activegcWeb/
    gen_cont_file_path = '/home/alxfed/archive/licensed_general_contractors.csv'
    input_columns = ['license_type', 'company_name', 'address', 'phone',
                     'license_expr', 'primary_insurance_expr',
                     'secondary_insurance_expr']
    output_columns = ['company_name', 'phone',
                      'street_address', 'city', 'state', 'zip',
                     'license_type',
                      'license_expr', 'primary_insurance_expr',
                     'secondary_insurance_expr']
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
        address = contractor['address'].replace('\xa0\xa0', '\xa0')
        street_address = ''; city = ''; state = ''; zip = ''
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
                                        con=conn, if_exists='replace')

    processed_gen_cont = '/home/alxfed/archive/licensed_general_contractors_database.csv'
    with open(processed_gen_cont, 'w') as f:
        f_csv = csv.DictWriter(f, output_columns)
        f_csv.writeheader()
        f_csv.writerows(all_rows)
    return


if __name__ == '__main__':
    main()
    print('main - done')