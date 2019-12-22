# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot


def main():
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    companies = pd.read_sql_table(table_name='companies', con=conn).astype(dtype=object)
    noted_companies = companies[companies['summary_note'].str.len() > 1]
    for indx, company in noted_companies.iterrows():
        res = hubspot.engagements.delete_an_engagement(company['summary_note'])
        print('ok', company['summary_note'])
    return


if __name__ == '__main__':
    main()
    print('main - done')