# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot


def main():
    # 0. Read the deals list;
    # 1. read the company from a deal;
    # 2. read associated contacts from this company;
    # 3. add contacts to the deal;

    conn_reference = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.CREATED_DEALS_TABLE, con=conn_reference)

    for index, deal in deals.iterrows():
        dealId = deal['dealId']  # text format
        companyId = str(int(deal['companyId'])) # because it is FLOAT in the db
        issue_date = deal['issue_date'] # datetime format

        contacts_list = hubspot.associations.get_associations_oauth(companyId, '2') # company to contact full

        result = hubspot.associations.create_one_to_many_associations(dealId, contacts_list, '3')

        if result:
            print(dealId, 'ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')