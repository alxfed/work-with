# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot


def main():
    # 1. get a companyId from a deal;
    # 2. read summary_note and summary_note_date from this company;
    # 3. if should not be updated - terminate, if should - step 4.
    # 4. read associated engagements from this company;
    # 5. chech if it has been done already and if not - add filtered engagements to the _company_.
    conn_reference = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.CREATED_DEALS_TABLE, con=conn_reference)

    for index, deal in deals.iterrows():
        dealId = deal['dealId']  # text format
        companyId = str(int(deal['companyId'])) # because it is FLOAT in the db
        issue_date = deal['issue_date'] # datetime format

        contacts_list = hubspot.associations.get_associations_oauth(companyId, '2') # company to contact full
        vice_versa = hubspot.associations.get_associations_oauth(companyId, '1') # empty

        result = hubspot.associations.create_one_to_many_associations(dealId, contacts_list, '3')

        deals_list = hubspot.associations.get_associations_oauth(companyId, '6') # company to deals - full
        # vice_veversa = hubspot.associations.get_associations_oauth(companyId, '5') # deal to company - empty
        #
        # eng_list = hubspot.engagements.get_engagements_of_object(companyId)
        # engagements = pd.DataFrame(eng_list, dtype=object)
        if result:
            print(dealId, 'ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')