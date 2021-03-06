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

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)
    companies['name'] = companies['name'].str.title()

    old_companies_permits = pd.DataFrame()
    new_companies = pd.DataFrame()
    not_found_companies = pd.DataFrame()
    seen_new_companies = set()
    seen_not_found = set()

    for index, this_permit in data.iterrows():
        # Debug for particular company
        # debug_company_name = 'Mk Construction'
        # debug_company = this_permit['name']
        # if debug_company_name in debug_company:
        #     print('ok')
        # Debug for particular company
        permit_to_add, company_to_add, not_found = sorting.companies.compare_permit_with_companies_and_reference(
            this_permit, companies, licensed_gen_contractors)
        if not company_to_add.empty:
            if not company_to_add['company_name'].values[0] in seen_new_companies:
                new_companies = new_companies.append(company_to_add, ignore_index=True)
                seen_new_companies.add(company_to_add['company_name'].values[0])
        if not permit_to_add.empty:
            old_companies_permits = old_companies_permits.append(permit_to_add, ignore_index=True)
        if not not_found.empty:
            if not not_found['name'].values[0] in seen_not_found:
                not_found_companies = not_found_companies.append(not_found, ignore_index=True)
                seen_not_found.add(not_found['name'].values[0])


    # upload them to the firstbase database
    conn_target = sqlalc.create_engine(sorting.PREP_DATABASE_URI) # thirdbase
    old_companies_permits.to_sql(
        name=sorting.OLD_COMPANIES_PERMITS_TABLE, # old_companies_permits
        con=conn_target, if_exists='replace', index=False)

    # unique
    if not not_found_companies.empty:
        not_found_companies.to_sql(
            name=sorting.NOT_FOUND_GENERAL_CONTRACTORS_TABLE, # not_found_general_contractors
            con=conn_target, if_exists='replace', index=False)

    if not new_companies.empty:
        conn_interm = sqlalc.create_engine(sorting.INTERM_DATABASE_URI) # secondbase
        new_companies.to_sql(
            name=sorting.NEW_COMPANIES_TABLE, # new_companies
            con=conn_interm, if_exists='replace', index=False)
    else:
        print('No new companies!')
    return


if __name__ == '__main__':
    main()
    print('main - done')