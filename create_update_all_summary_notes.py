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
    # 1. get a deal in a Sales Pipeline state;
    # 2. find a unprocessed company for this deal;
    # 2. get summary_note_number and summary_note_date_str from this company;
    # 3. if should not be updated - terminate, if should - step 4.
    # 4. read associated engagements from this company;
    # 5. check if it has been done already and if not - add filtered engagements to the _company_.

    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_deals = pd.read_sql_table(table_name=sorting.DEALS_TABLE, con=conn_source)

    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_companies = pd.read_sql_table(table_name=sorting.COMPANIES_TABLE, con=conn_reference)

    # df.loc[df['column_name'].isin(some_values)]
    deals = all_deals[all_deals['dealstage'].isin(hubspot.constants.NAMES_OF_STATES.keys())] # only the Sales Pipeline

    processed_companies = set() # unique companies also, see: https://stackoverflow.com/questions/10547343/add-object-into-pythons-set-collection-and-determine-by-objects-attribute
    start_index = 0          # restart an interrupted execution from here.

    for index, deal in deals.iterrows():
        if index >= start_index:
            dealId = deal['dealId']
            print('Now working on deal ', dealId)
            co_id_rec = deal['associatedCompanyIds']
            if co_id_rec:
                companyId = int(co_id_rec)
                if not companyId in processed_companies:
                    processed_companies.add(companyId)
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
                        print('Company for this deal not found')
                else:
                    print('One more deal of:  ', companyId)
            else:
                print('No companyId for deal: ', dealId)
        else:
            pass
    return


if __name__ == '__main__':
    main()
    print('main - done')
