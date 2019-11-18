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
    input_file_path = '/home/alxfed/archive/licensed_general_contractors.csv'
    gen_cont_file_path = '/home/alxfed/archive/licensed_general_contractors.csv'
    processed_gen_cont = '/home/alxfed/archive/licensed_general_contractors_database.csv'

    conn_home = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    reference_columns = ['company_name', 'phone',
                      'street_address', 'city', 'state', 'zip',
                     # 'license_type',
                      'license_expr'] #, 'primary_insurance_expr',
                     #'secondary_insurance_expr']
    licensed = pd.read_sql_table(table_name='licensed_general_contractors',
                                 con=conn_home,
                                 columns=reference_columns)

    input_columns = ['license_type', 'company_name', 'address', 'phone',
                     'license_expr', 'primary_insurance_expr',
                     'secondary_insurance_expr']

    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')