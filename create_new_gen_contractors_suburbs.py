# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import hubspot
import sqlalchemy as sqlalc
import sorting


def main():
    params = {
                    'name': '',
                    'type':'PROSPECT',
                    'phone':'',
                    'address':'',
                    'city':'',
                    'state':'',
                    'zip': '',
                    'category':'gen_contractor_suburbs',
                    'website': ''
                  }

    conn_source = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)
    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)

    companies = pd.read_sql_table(
        table_name=sorting.USABLE_VERIGOOGED_GENERAL, con=conn_source)

    created_companies = pd.DataFrame()

    for indx, company in companies.iterrows():
        # created_co = pd.DataFrame()
        # company['companyId'].append({'companyId': 246})
        parameters = params.copy()
        parameters['name'] = company['name']
        parameters['phone'] = company['formatted_phone_number']
        parameters['address'] = company['formatted_address']
        parameters['website'] = company['website']
        parameters['elgoog_place_id'] = company['place_id']
        parameters['elgoog_types'] = company['types']
        done = hubspot.companies.create_company(parameters)
        if done:
            company = company.append(pd.Series({'companyId': done['companyId']}))
            created_companies = created_companies.append(company, ignore_index=True)
            print('Created:  ', parameters['name'])
        else:
            print('Did not create ', parameters['name'])

    created_companies.to_sql(
        name=sorting.CREATED_SUBURBAN_COMPANIES_TABLE,
        con=conn_result, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')