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
                    'category':'General Contractor'
                  }

    conn_source = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)
    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)

    companies = pd.read_sql_table(
        table_name=sorting.NEW_COMPANIES_TABLE, con=conn_source)

    created_companies = pd.DataFrame()

    for indx, company in companies.iterrows():
        # created_co = pd.DataFrame()
        # company['companyId'].append({'companyId': 246})
        parameters = params.copy()
        co_name = company['company_name']
        parameters['name'] = co_name
        parameters['city'] = company['city']
        parameters['phone'] = company['phone']
        parameters['address'] = company['street_address']
        parameters['state'] = company['state']
        parameters['zip'] = company['zip']
        done = hubspot.companies.create_company(parameters)
        if done:
            company = company.append(pd.Series({'companyId': done['companyId']}))
            created_companies = created_companies.append(company, ignore_index=True)
            print('Created:  ', parameters['name'])
        else:
            print('Did not create ', parameters['name'])

    created_companies.to_sql(
        name=sorting.CREATED_COMPANIES_TABLE,
        con=conn_result, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')