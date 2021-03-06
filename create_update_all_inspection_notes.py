# -*- coding: utf-8 -*-
"""https://jsonlines.readthedocs.io/en/latest/
"""
import jsonlines
import pandas as pd
import hubspot
import datetime as dt
import sorting
import sqlalchemy as sqlalc


def main():
    # update the inspection notes, create new if don't exist
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI) # 'sqlite:////home/alxfed/dbase/home.sqlite'
    existing_notes = pd.read_sql_table(
        table_name=sorting.CREATED_INSPECTION_NOTES, con=conn_reference) # 'created_insp_notes'
    all_deals = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn_reference) # 'deals',
    ''' Parameters on a deal:
    'insp_note': inspection_note,
    'insp_n': last_inspection_number,
    'last_inspection': last_inspection_type,
    'last_inspection_date': hubspot_timestamp
    '''
    SOURCE_FILE = '/home/alxfed/archive/last_deals_inspections.jl'

    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)

    with jsonlines.open(SOURCE_FILE, mode='r') as reader:
        for line in reader:
            permit = line['permit']
            deal = all_deals[all_deals['permit_'] == permit].iloc[0]
            if not deal.empty:
                dealId                  = deal['dealId']
                insp_note               = deal['insp_note']
                insp_n                  = deal['insp_n']
                last_inspection         = deal['last_inspection']
                last_inspection_date    = deal['last_inspection_date']
                dealDate                = deal['permit_issue_date']
                if not dealDate:
                    date = pd.Timestamp(1562950000000, unit='ms', tz='US/Central')
                    # date = pd.Timestamp(2019, 7, 12, 12)
                else:
                    date = dealDate
                if insp_note: # the inspections note exists
                    inote = sorting.inspections.InspectionsNote(
                        dealId=dealId, engagementId=insp_note, insp_n=insp_n, last_inspection=last_inspection,
                        last_inspection_date=last_inspection_date)
                    inote.prepare_note(line, date)
                    if inote.ready:
                        inote.update()
                    else:
                        print('Not updated, because the note for ', dealId, ' was not ready')
                else: # the inspections note doesn't exist
                    inote = sorting.inspections.InspectionsNote(dealId=dealId)
                    inote.prepare_note(line, date)
                    if inote.ready:
                        inote.create()
                    else:
                        print('Not created, because the note for ', dealId, ' would be empty')
            else: # no deal for the scraped permit, nothing to post to
                print('No deal for scraped permit #', permit)
                pass
    reader.close()
    return


if __name__ == '__main__':
    main()
    print('done')
