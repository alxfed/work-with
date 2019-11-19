# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
import sqlalchemy as sqlalc


def getPandasSchema(df):
    ''' takes a pandas dataframe and returns the dtype dictionary
    useful for applying types when reloading that dataframe from csv etc
    '''
    return dict(zip(df.columns.tolist(),df.dtypes.tolist()))


def main():
    # all companies from HubSpot
    downuploaded_companies = '/home/alxfed/archive/companies_database.csv'

    request_params = ['name', 'phone', 'phone_mobile', 'phone_voip',
                      'phone_toll','phone_landline','phone_unidentified',
                      'address','city','zip','state', 'category','website']

    normal_columns = ['companyId', 'isDeleted', 'name', 'phone',
                      'address', 'city', 'zip', 'state',
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

    meta = getPandasSchema(all_companies)

    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    all_companies.to_sql(name='companies', con=conn, if_exists='replace',
                         index=False)

    with open(downuploaded_companies, 'w') as f:
        f_csv = csv.DictWriter(f, all_columns)
        f_csv.writeheader()
        f_csv.writerows(all_companies_cdr)
    return


if __name__ == '__main__':
    main()
    print('main - done')
