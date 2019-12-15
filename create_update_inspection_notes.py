# -*- coding: utf-8 -*-
"""https://jsonlines.readthedocs.io/en/latest/
"""
import jsonlines
import pandas as pd
import hubspot
import datetime as dt
import sorting
import sqlalchemy as sqlalc


def post_permit_inspections(scraped_line, date, dealId):
    inspections_table = pd.DataFrame()
    last_inspection = pd.DataFrame()
    insp_table = pd.DataFrame.from_records(scraped_line['insp_table'])
    if not insp_table.empty:  # any inspections at all in this record? Otherwise - why bother?
        if 'insp_date' in insp_table.keys():  # there is a table and it has 'insp_date' column
            insp_table['insp_date'] = pd.to_datetime(insp_table['insp_date'], infer_datetime_format=True)
            inspections_table = insp_table[insp_table['insp_date'] >= date]
            if not inspections_table.empty:
                last_inspection = inspections_table.iloc[0]
            else:
                print('No inspections after permit for deal', dealId)
        else:  # there is an ispection with number but no date column? Really?
            pass
    else:  # inspections table is empty
        pass
    return inspections_table, last_inspection


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI) # 'sqlite:////home/alxfed/dbase/home.sqlite'
    existing_notes = pd.read_sql_table(
        table_name=sorting.CREATED_INSPECTION_NOTES, con=conn_reference) # 'created_insp_notes'
    all_deals = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn_reference) # 'deals',

    SOURCE_FILE = '/home/alxfed/archive/last_deals_inspections.jl'

    # permit, dealId, (note) id
    ownerId = 40202623  # Data Robot

    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)


    # permit_inspections = ['PERMIT INSPECTION', 'BLDG_PERM IRON PERMIT INSP', 'VENT/HEAT PERMIT INSPECTION',
    #                       'WATER DEPT PERMIT INSPECTION', 'ELECTRICAL PERMIT INSPECTION', 'CONSTRUCTION EQUIPMENT PERMIT',
    #                       'PORCH/DECK PERMIT INSPECTION', 'BLDG_PERM IRON PERMIT INSP', 'BOILER PERMIT INSPECTION',
    #                       'DOB NEW CONSTRUCTION INSP', 'DOB PLUMBING INSPECTION', 'DOB VENT/FURNACE INSPECTION',
    #                       'DOB REFRIGERATION INSPECTION', 'DOB GARAGE INSPECTION',
    #                       'EQUIPMENT INSPECTION']
    created_notes_for_permits = existing_notes['permit_'].to_list()

    with jsonlines.open(SOURCE_FILE, mode='r') as reader:
        for line in reader:
            has_data = True
            permit = line['permit']
            deal = all_deals[all_deals['permit_'] == permit]
            if not deal.empty:
                dealId = deal['dealId'].values[0]
                dealDate = deal['permit_issue_date']
                if dealDate.empty:
                    date = dt.datetime(year=2019, month=7, day=12, hour=0, minute=0, second=0)
                else:
                    date = dealDate.values[0]
                post_permit_inspections_table, last_inspection_table = post_permit_inspections(line, date, dealId)
                if not post_permit_inspections_table.empty:
                    last_inspection_date = last_inspection_table['insp_date']
                    last_inspection_type = last_inspection_table['type_desc']
                    last_inspection_number = last_inspection_table['insp_n']
                    hubspot_timestamp = int(last_inspection_date.timestamp() * 1000)
                    # update the deal parameters last_inspection and last_inspection_date here
                    result = hubspot.deals.update_a_deal_oauth(dealId, {'last_inspection': last_inspection_type.title(),
                                                                        'last_inspection_date': hubspot_timestamp})
                    if result:
                        print('Updated a deal: ', dealId)
                    post_permit_inspections_table['insp_date'] = post_permit_inspections_table['insp_date'].dt.strftime('%Y-%m-%d')
                    note_text = post_permit_inspections_table.to_html(header=False, index=False)
                # branching for existent and non-existent - here
                    params = {'ownerId': ownerId, 'timestamp': hubspot_timestamp, 'dealId': dealId, 'note': note_text}
                    created_note = hubspot.engagements.create_engagement_note(params)
                    creupdated_note = created_note['engagement']
                    creupdated_note.update({'permit': permit, 'dealId': dealId,
                                       'insp_n': last_inspection_number, 'insp_date': hubspot_timestamp,
                                       'insp_type': last_inspection_type})
                    # log the line
                    note = pd.DataFrame()
                    note.to_sql(
                        name=sorting.INSPECTION_NOTES,
                        con=conn_result, if_exists='append', index=False)
                else:
                    print('No inspections after permit for deal: ', dealId)
            else: # no deal for the scraped permit, nothing to post to
                print('No deal for scraped permit #', permit)
                pass
    reader.close()
    return


if __name__ == '__main__':
    main()
    print('main - done')
