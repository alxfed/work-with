# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.SOURCE_DATABASE_URI)
    data = pd.read_sql_table(table_name=sorting.NEW_PERMITS_TABLE, con=conn_source)
    licensed_gen_contractors = pd.read_sql_table(table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_source)
    companies = pd.read_sql_table(table_name=sorting.COMPANIES_TABLE, con=conn_source)

    # reference list of existing companies
    companies_list = companies['name'].to_list()

    # big new permits for New Construction and Renovation/Alteration
    data_big = data[(data['reported_cost'] > 100000) &
                    ((data['permit_type'] == 'PERMIT - NEW CONSTRUCTION') |
                    (data['permit_type'] == 'PERMIT - RENOVATION/ALTERATION'))]

    # general contractors for these permits
    gen_contractors = sorting.companies.extract_general_contractors_out_of_new_permits(data_big)
    gen_contractors['name'] = gen_contractors['name'].str.title()
    gen_contractors['city'] = gen_contractors['city'].str.title()
    unique_gen_contractors = pd.DataFrame(gen_contractors['name'].unique(), columns=['name'])

    # upload them to the firstbase database
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    gen_contractors.to_sql(name=sorting.GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE, con=conn_target,
                           if_exists='replace', index=False)
    unique_gen_contractors.to_sql(name=sorting.UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE, con=conn_target,
                           if_exists='replace', index=False)

    # upload to the next stage database
    result = pd.DataFrame()
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    result.to_sql(name=sorting.NEW_COMPANIES_TABLE, con=conn_target, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')