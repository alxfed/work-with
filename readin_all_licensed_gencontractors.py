# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import csv
import sqlalchemy as sqlalc
import sorting


def main():
    # all licensed general contractors from the site https://webapps1.chicago.gov/activegcWeb/
    gen_cont_file_path = '/home/alxfed/archive/licensed_general_contractors_results.csv'

    normal_columns = ['company_name', 'street_address', 'phone', 'city', 'state', 'zip', 'license_type', 'license_expr',
                      'primary_insurance_expr', 'secondary_insurance_expr']

    all_licensed_gencontractors = pd.read_csv(gen_cont_file_path, usecols= normal_columns,
                                              parse_dates=['license_expr',
                                                           'primary_insurance_expr',
                                                           'secondary_insurance_expr'],
                                              dtype=object)
    # FORMATTING!
    all_licensed_gencontractors['company_name'] = all_licensed_gencontractors['company_name'].str.strip()
    all_licensed_gencontractors['company_name'] = all_licensed_gencontractors['company_name'].str.title()
    all_licensed_gencontractors['city'] = all_licensed_gencontractors['city'].str.title()
    all_licensed_gencontractors['street_address'] = all_licensed_gencontractors['street_address'].str.title()

    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_licensed_gencontractors.to_sql(name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE,
                                       con=conn, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')
