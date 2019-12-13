# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)

    data = pd.read_sql_table(
        table_name=sorting.NEW_PERMITS_WITH_GENERAL_CONTRACTORS_TABLE, con=conn_source)

    licensed_gen_contractors = pd.read_sql_table(
        table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_reference)
    licensed_gen_contractors['company_name'] = licensed_gen_contractors['company_name'].str.title()

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)



    old_companies_permits = pd.DataFrame()
    new_companies = pd.DataFrame()
    not_found_companies = pd.DataFrame()

    for index, this_permit in data.iterrows():
        # Debug for particular company
        debug_company_name = 'Mk Construction'
        debug_company = this_permit['name']
        if debug_company_name in debug_company:
            print('ok')
        # Debug for particular company
        not_to_add, company_to_add, not_found = sorting.companies.compare_with_companies_and_reference(
            this_permit, companies, licensed_gen_contractors)
        if not company_to_add.empty:
            new_companies = new_companies.append(company_to_add, ignore_index=True)
        if not not_to_add.empty:
            old_companies_permits = old_companies_permits.append(not_to_add, ignore_index=True)
        if not not_found.empty:
            not_found_companies = not_found_companies.append(not_found, ignore_index=True)

    # upload them to the firstbase database
    conn_target = sqlalc.create_engine(sorting.PREP_DATABASE_URI)
    gen_cons_with_permits.to_sql(
        name=sorting.GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    unique_gen_contractors.to_sql(
        name=sorting.UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    old_companies_permits.to_sql(
        name=sorting.OLD_COMPANIES_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    new_companies.to_sql(
        name=sorting.NEW_COMPANIES_TABLE,
        con=conn_target, if_exists='replace', index=False)

    # upload to the next stage database
    # result = pd.DataFrame()
    # conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    # result.to_sql(name=sorting.NEW_COMPANIES_TABLE, con=conn_target, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')