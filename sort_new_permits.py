# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def main():
    # read the downuploaded table of new_permits
    conn_source = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)

    data = pd.read_sql_table(
        table_name=sorting.NEW_PERMITS_TABLE, con=conn_source)


    # big new permits for New Construction and Renovation/Alteration
    data_big = data[(data['reported_cost'] > 100000) &
        ((data['permit_type'] == 'PERMIT - NEW CONSTRUCTION') |
        (data['permit_type'] == 'PERMIT - RENOVATION/ALTERATION'))]

    # general contractors for these permits
    gen_cons_with_permits = sorting.companies.general_contractors_and_permits(data_big)
    gen_cons_with_permits['suffix'] = gen_cons_with_permits['suffix'].str.title() # because in companies it stops on Nones
    unique_gen_contractors = pd.DataFrame(
        gen_cons_with_permits['name'].unique(), columns=['name'])

    # upload them to the firstbase database
    conn_target = sqlalc.create_engine(sorting.TARGET_DATABASE_URI)
    gen_cons_with_permits.to_sql(
        name=sorting.NEW_PERMITS_WITH_GENERAL_CONTRACTORS_TABLE,
        con=conn_target, if_exists='replace', index=False)
    unique_gen_contractors.to_sql(
        name=sorting.UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE,
        con=conn_target, if_exists='replace', index=False)

    return


if __name__ == '__main__':
    main()
    print('main - done')