# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot
import datetime as dt
from sorting.summary import SummaryNote


def main():
    # 1. get a companyId from a deal;
    # 2. read summary_note and summary_note_date from this company;
    # 3. if should not be updated - terminate, if should - step 4.
    # 4. read associated engagements from this company;
    # 5. check if it has been done already and if not - add filtered engagements to the _company_.

    conn_source = sqlalc.create_engine(sorting.INTERM_DATABASE_URI)
    all_deals = pd.read_sql_table(table_name=sorting.FRESH_DEALS_TABLE, con=conn_source)

    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_companies = pd.read_sql_table(table_name=sorting.COMPANIES_TABLE, con=conn_reference)
    all_companies['companyId'] = all_companies['companyId'] # .astype(dtype=object)

    deals = all_deals[all_deals['associatedCompanyIds'] != ''] # exclude deals with individuals

    companies = set() # unique companies also, see: https://stackoverflow.com/questions/10547343/add-object-into-pythons-set-collection-and-determine-by-objects-attribute

    for index, deal in deals.iterrows():
        dealId = deal['dealId']
        companyId = int(deal['associatedCompanyIds'])
        if not companyId in companies:
            companies.add(companyId)
            co_info = all_companies[all_companies['companyId'] == companyId]
            if not co_info.empty:
                summary_note = co_info['summary_note_number'].values[0]
                summary_note_timestamp = co_info['summary_note_date_str'].values[0]
                if summary_note:
                    now = int(1000 * dt.datetime.now().timestamp())
                    if (now - int(summary_note_timestamp)) > 10000000:
                        old_note = SummaryNote(companyId=companyId,
                                               engagementId=summary_note)
                        old_note.prepare_note()
                        if old_note.ready:
                            res = old_note.update()
                    else:
                        print('Too early to update')
                else:  # summary note doesn't exist
                    note = SummaryNote(companyId=companyId)
                    note.prepare_note()
                    if note.ready:
                        res = note.create()
                    else:
                        print('The note would be empty')
                        del note
            else:
                # no company info. what kind of a company is that?
                # Somethin's not working properly. Stop!
                print('Company for this deal not found')
        else:
            # company has been processed.
            print('One more deal of:  ', companyId)
    return


if __name__ == '__main__':
    main()
    print('main - done')
