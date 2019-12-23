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
                        # old_note = SummaryNote(companyId=companyId,
                        #                        engagementId=summary_note,
                        #                        hs_timestamp=summary_note_timestamp)
                        # old_note.prepare_note()
                        # if old_note.ready:
                        #     res = old_note.update(timestamp=str(now))
                        pass
                else:  # summary note doesn't exist
                    note = SummaryNote(companyId=companyId)
                    note.prepare_note()
                    if note.ready:
                        res = note.create()
                    else:
                        print('Note is empty')
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


'''
'hs_object_id': 
    {'value': '436812705', 
    'timestamp': 1545070632884, 
    'source': 'CALCULATED', 
    'sourceId': None, 
    'versions': [{'name': 'hs_object_id', 'value': '436812705', 'timestamp': 1545070632884, 'source': 'CALCULATED', 'sourceVid': []}]
    }, 
'hs_analytics_source_data_2': 
    {'value': 'CRM_UI', 
    'timestamp': 1557852770795, 
    'source': 'DEALS', 
    'sourceId': 'deal sync triggered by company id=1114608131', 
    'versions': [{'name': 'hs_analytics_source_data_2', 'value': 'CRM_UI', 'timestamp': 1557852770795, 'sourceId': 'deal sync triggered by company id=1114608131', 'source': 'DEALS', 'sourceVid': []}]
    }, 
'hs_analytics_source_data_1': 
    {'value': 'CONTACTS', 
    'timestamp': 1557852770795, 
    'source': 'DEALS', 'sourceId': 
    'deal sync triggered by company id=1114608131', 
    'versions': [{'name': 'hs_analytics_source_data_1', 'value': 'CONTACTS', 'timestamp': 1557852770795, 'sourceId': 'deal sync triggered by company id=1114608131', 'source': 'DEALS', 'sourceVid': []}]}
    },
'imports': [], 
'stateChanges': []
'''

'''
                    post_permit_inspections_table, last_inspection_table = post_permit_inspections(line, date, dealId)
                    if not post_permit_inspections_table.empty:
                        last_inspection_number = last_inspection_table['insp_n']
                        recorded_inspection = str(deal['insp_n'].values[0])
                        inspection_note = str(deal['insp_note'].values[0])
                        if not last_inspection_number == recorded_inspection:
                            last_inspection_date = last_inspection_table['insp_date']
                            last_inspection_type = last_inspection_table['type_desc']
                            hubspot_timestamp = int(last_inspection_date.timestamp() * 1000)
                            post_permit_inspections_table['insp_date'] = post_permit_inspections_table['insp_date'].dt.strftime('%Y-%m-%d')
                            note_text = post_permit_inspections_table.to_html(header=False, index=False)
                            # branching for existent and non-existent - here
                            if inspection_note:
                                params = {'timestamp': hubspot_timestamp, 'note': note_text}
                                res = hubspot.engagements.update_an_engagement(inspection_note, params)
                                if res:
                                    print('updated the note ', inspection_note)
                                    # update the deal parameters last_inspection and last_inspection_date here
                                    result = hubspot.deals.update_a_deal_oauth(dealId, {
                                        'last_inspection': last_inspection_type.title(),
                                        'last_inspection_date': hubspot_timestamp,
                                        'insp_n': last_inspection_number})
                                    if result:
                                        print('Updated deal: ', dealId)
                                else:
                                    print('did not update the note', id)
                            else:
                                params = {'ownerId': ownerId, 'timestamp': hubspot_timestamp, 'dealId': dealId, 'note': note_text}
                                cre = hubspot.engagements.create_engagement_note(params)
                                if cre:
                                    created_note = cre['engagement']
                                    inspection_note = created_note['id']
                                    result = hubspot.deals.update_a_deal_oauth(dealId, {'insp_note': inspection_note,
                                                                                        'insp_n': last_inspection_number,
                                                                                        'last_inspection': last_inspection_type.title(),
                                                                                        'last_inspection_date': hubspot_timestamp})
                                    if result:
                                        print('Updated deal: ', dealId)
                            note = pd.DataFrame()
                            # note.to_sql(name=sorting.INSPECTION_NOTES,
                            #             con=conn_result, if_exists='append', index=False)
                        else:
                            print('The last inspection number is the same. No new inspections. Nothing to update.')
                    else:
                        print('No inspections after permit for deal: ', dealId)

'''