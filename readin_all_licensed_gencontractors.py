# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import csv
import sqlalchemy as sqlalc
import numpy as np


def main():
    # all licensed general contractors from the site https://webapps1.chicago.gov/activegcWeb/
    gen_cont_file_path = '/home/alxfed/archive/general_contractors_results.csv'

    normal_columns = ['company_name', 'street_address', 'phone', 'city', 'state', 'zip', 'license_type', 'license_expr',
                      'primary_insurance_expr', 'secondary_insurance_expr']

    all_licensed_gencontractors = pd.read_csv(gen_cont_file_path, usecols= normal_columns,
                                              parse_dates=['license_expr',
                                                           'primary_insurance_expr',
                                                           'secondary_insurance_expr'],
                                              dtype=object)

    # all_licensed_gencontractors.fillna(value='', inplace=True)

    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    all_licensed_gencontractors.to_sql(name='all_licensed_general_contractors', con=conn, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')
