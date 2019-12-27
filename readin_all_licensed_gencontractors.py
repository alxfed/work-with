# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
from numpy import nan
import sqlalchemy as sqlalc
import sorting
from datetime import datetime


def dateparse(x):
    if x is nan:
        return datetime(2018, 12, 8, 0, 0)
    else:
        return pd.datetime.strptime(x, '%m/%d/%y') #  %H:%M:%S.%f if there are hours, minutes, seconts and milliseconds


def main():
    # all licensed general contractors from the site https://webapps1.chicago.gov/activegcWeb/
    # scraped to the /home/alxfed/archive/licensed_general_contractors_results.csv file
    # will now be transferred into the center database. From there it will be processed and put
    # into home database and firstbase.
    gen_cont_file_path = '/home/alxfed/archive/licensed_general_contractors_results.csv'

    normal_columns = ['company_name', 'street_address', 'phone', 'city', 'state', 'zip', 'license_type', 'license_expr',
                      'primary_insurance_expr', 'secondary_insurance_expr']

    all_licensed_gencontractors = pd.read_csv(gen_cont_file_path, usecols= normal_columns,
                                              parse_dates=['license_expr',  # right now doesn't work. dd/mm/YYYY format
                                                           'primary_insurance_expr',
                                                           'secondary_insurance_expr'],
                                              # date_parser=dateparse,
                                              dtype=object)
    # FORMATTING!
    all_licensed_gencontractors['company_name'] = all_licensed_gencontractors['company_name'].str.strip()
    all_licensed_gencontractors['company_name'] = all_licensed_gencontractors['company_name'].str.title()
    all_licensed_gencontractors['city'] = all_licensed_gencontractors['city'].str.title()
    all_licensed_gencontractors['street_address'] = all_licensed_gencontractors['street_address'].str.title()
    all_licensed_gencontractors['zip'].replace("-\d?\d+", '', inplace=True, regex=True)
    all_licensed_gencontractors['zip'].replace('-', '', inplace=True, regex=True)

    conn = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)
    all_licensed_gencontractors.to_sql(name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE,
                                       con=conn, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')
