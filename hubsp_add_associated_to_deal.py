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
    # 3. read associated engagements from this company;
    # 4. add contacts to the deal;
    # 5. add filtered engagements to the deal.
    conn_reference = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.CREATED_DEALS_TABLE, con=conn_reference)

    for index, deal in deals.iterrows():
        dealId = deal['dealId']  # text format
        companyId = str(int(deal['companyId'])) # because it is FLOAT in the db
        issue_date = deal['issue_date'] # datetime format

        contacts_list = hubspot.associations.get_associations_oauth(companyId, '2') # company to contact full
        vice_versa = hubspot.associations.get_associations_oauth(companyId, '1') # empty

        deals_list = hubspot.associations.get_associations_oauth(companyId, '5') # deal to company - empty
        vice_veversa = hubspot.associations.get_associations_oauth(companyId, '6') # company to deals - full

        eng_list = hubspot.engagements.get_engagements_of_object(companyId)
        engagements = pd.DataFrame(eng_list, dtype=object)
        print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')