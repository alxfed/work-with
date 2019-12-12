# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def compare_with_companies_and_reference(row, present, reference):
    # reference - licensed general contractors in the official list
    # present - companies in the system
    # row - permit
    to_add = pd.DataFrame()
    not_to_add = pd.DataFrame()

    co_name, sep, dba  = row['name'].partition(' Dba ')  # split if there is a dba, then sep and dba are nonzero
    # va = present['name'].values
    found = present[present['name'].str.find(sub=co_name) != -1]
    if found.empty:
        not_to_add = not_to_add.append(row)
        print('Did not find ', row['general_contractor'], ' in the list of companies')
        print('Adding it to the not create file \n')
        pass
    else:
        to_add = to_add.append(row)
        to_add['companyId'] = found['companyId'].values[0]
        pass

    return to_add, not_to_add


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.SOURCE_DATABASE_URI)

    data = pd.read_sql_table(
        table_name=sorting.NEW_PERMITS_TABLE, con=conn_source)
    licensed_gen_contractors = pd.read_sql_table(
        table_name=sorting.LICENSED_GENERAL_CONTRACTORS_TABLE, con=conn_source)
    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_source)

    # reference list of existing companies
    # companies_list = companies['name'].to_list()

    # big new permits for New Construction and Renovation/Alteration
    data_big = data[(data['reported_cost'] > 100000) &
        ((data['permit_type'] == 'PERMIT - NEW CONSTRUCTION') |
        (data['permit_type'] == 'PERMIT - RENOVATION/ALTERATION'))]

    # general contractors for these permits
    gen_cons_with_permits = sorting.companies.general_contractors_and_permits(data_big)
    gen_cons_with_permits['name'] = gen_cons_with_permits['name'].str.title()
    gen_cons_with_permits['city'] = gen_cons_with_permits['city'].str.title()
    gen_cons_with_permits['street_name'] = gen_cons_with_permits['street_name'].str.title()
    gen_cons_with_permits['suffix'] = gen_cons_with_permits['suffix'].str.title()
    unique_gen_contractors = pd.DataFrame(
        gen_cons_with_permits['name'].unique(), columns=['name'])

    new_companies_permits = pd.DataFrame()
    old_companies_permits = pd.DataFrame()

    for index, this_permit in gen_cons_with_permits.iterrows():
        to_add, not_to_add = compare_with_companies_and_reference(
            this_permit, companies, licensed_gen_contractors)
        if to_add.empty:
            old_companies_permits = old_companies_permits.append(not_to_add, ignore_index = True)
        elif not_to_add.empty:
            new_companies_permits = new_companies_permits.append(to_add, ignore_index=True)

    # upload them to the firstbase database
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    gen_cons_with_permits.to_sql(
        name=sorting.GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    unique_gen_contractors.to_sql(
        name=sorting.UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    old_companies_permits.to_sql(
        name=sorting.OLD_COMPANIES_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    new_companies_permits.to_sql(
        name=sorting.NEW_COMPANIES_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)

    # upload to the next stage database
    # result = pd.DataFrame()
    # conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    # result.to_sql(name=sorting.NEW_COMPANIES_TABLE, con=conn_target, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')