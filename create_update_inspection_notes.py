# -*- coding: utf-8 -*-
"""https://jsonlines.readthedocs.io/en/latest/
"""
import jsonlines
import pandas as pd
import hubspot
import datetime as dt
import sorting
import sqlalchemy as sqlalc


def post_permit_inspections(scraped_line, ):
    insp_table = pd.DataFrame.from_records(scraped_line['insp_table'])
    return


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI) # 'sqlite:////home/alxfed/dbase/home.sqlite'
    existing_notes = pd.read_sql_table(
        table_name=sorting.CREATED_INSPECTION_NOTES, con=conn_reference) # 'created_insp_notes'
    all_deals = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn_reference) # 'deals',

    SOURCE_FILE = '/home/alxfed/archive/last_deals_inspections.jl'

    # permit, dealId, (note) id
    ownerId = 40202623  # Data Robot

    # permit_inspections = ['PERMIT INSPECTION', 'BLDG_PERM IRON PERMIT INSP', 'VENT/HEAT PERMIT INSPECTION',
    #                       'WATER DEPT PERMIT INSPECTION', 'ELECTRICAL PERMIT INSPECTION', 'CONSTRUCTION EQUIPMENT PERMIT',
    #                       'PORCH/DECK PERMIT INSPECTION', 'BLDG_PERM IRON PERMIT INSP', 'BOILER PERMIT INSPECTION',
    #                       'DOB NEW CONSTRUCTION INSP', 'DOB PLUMBING INSPECTION', 'DOB VENT/FURNACE INSPECTION',
    #                       'DOB REFRIGERATION INSPECTION', 'DOB GARAGE INSPECTION',
    #                       'EQUIPMENT INSPECTION']

    with jsonlines.open(SOURCE_FILE, mode='r') as reader:
        for line in reader:
            has_data = True
            permit = line['permit']
            created_notes_for_permits = existing_notes['permit_'].to_list()
            if permit in created_notes_for_permits: # TODO here's the update part of the program
                has_data = False
                print('Already created a note for permit #  ', permit)
            else:   # get deal parameter from the reference
                deal_line = all_deals[all_deals['permit_'] == permit]
                if deal_line.empty:
                    print('No deal for permit #  ', permit)
                    has_data = False
                else:
                    dealId = deal_line['dealId'].values[0] # 1143450728
                    date = pd.to_datetime(deal_line['permit_issue_date'], infer_datetime_format=True).values[0]
                    insp_table = pd.DataFrame.from_records(line['insp_table'])
                    if insp_table.empty:
                        print('No data about inspections for deal', dealId)
                        has_data = False
                    elif 'insp_date' in insp_table.keys():
                        insp_table['insp_date'] = pd.to_datetime(insp_table['insp_date'], infer_datetime_format=True)
                        post_permit = insp_table[insp_table['insp_date'] >= date]
                        if not post_permit.empty:
                            last_inspection = post_permit.iloc[0]
                            last_inspection_datetime = last_inspection['insp_date']
                            last_inspection_number = last_inspection['insp_n']
                            last_inspection_type = last_inspection['type_desc']
                        else:
                            print('No inspections after permit for deal', dealId)
                            has_data = False
                    else:
                        post_permit = insp_table
                        last_inspection = post_permit.iloc[0]
                        last_inspection_type = last_inspection['type_desc']
                        last_inspection_number = last_inspection['insp_n']
                        last_inspection_datetime = dt.datetime(year=2019, month=7, day=12, hour=0, minute=0, second=0)
                    if has_data:
                        hubspot_timestamp = int(last_inspection_datetime.timestamp() * 1000)
                        # update the deal parameters last_inspection and last_inspection_date here
                        result = hubspot.deals.update_a_deal_oauth(dealId, {'last_inspection': last_inspection_type.title(),
                                                                            'last_inspection_date': hubspot_timestamp})
                        if result:
                            print('Updated a deal: ', dealId)
                        else:
                            print('Did not update the deal: ', dealId)
                        post_permit['insp_date'] = post_permit['insp_date'].dt.strftime('%Y-%m-%d')
                        note_text = post_permit.to_html(header=False, index=False)
                        params = {'ownerId': ownerId, 'timestamp': hubspot_timestamp, 'dealId': dealId,
                                  'note': note_text}
                        created_note = hubspot.engagements.create_engagement_note(params)
                        engagement = created_note['engagement']
                        engagement.update({'permit': permit, 'dealId': dealId,
                                           'insp_n': last_inspection_number, 'insp_date': hubspot_timestamp,
                                           'insp_type': last_inspection_type})
                        # transform
                        # TODO line writer was here writer.write(engagement)
    reader.close()
    return

'''
perm_table = pd.DataFrame.from_records(line['perm_table'])
perm_table['perm_date'] = pd.to_datetime(perm_table['perm_date'], infer_datetime_format=True)
permeat = perm_table.loc[perm_table['permit_n'] == permit]
if permeat.empty:
    print('No such permit on page ', permit)
    break
date = permeat['perm_date'].values[0] 
'''

if __name__ == '__main__':
    main()
    print('main - done')
