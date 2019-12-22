# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
import sqlalchemy as sqlalc
import sorting


def main():
    # all deals from HubSpot
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn)
    # Sales = default
    # New Construction/Renovation/Alteration = 815585
    downuploaded_deals = '/home/alxfed/archive/deals_database.csv'
    request_params = ['dealname', 'description', 'design_date',
                      'closedate', 'amount', 'pipeline', 'dealstage',
                      'permit_issue_date', 'permit_', 'permit', 'permit_type',
                      'work_descrption',
                      'last_inspection', 'last_inspection_date', 'insp_n', 'insp_note']
    normal_columns = ['dealId', 'isDeleted',
                      'dealname', 'description', 'design_date',
                      'closedate', 'amount', 'pipeline', 'dealstage',
                      'permit_issue_date', 'permit_', 'permit', 'permit_type',
                      'work_descrption',
                      'last_inspection', 'last_inspection_date', 'insp_n', 'insp_note']
    include_associations = True

    all_deals_cdr, all_columns = hubspot.deals.get_all_deals_oauth(request_params, include_associations)
    all_deals = pd.DataFrame(all_deals_cdr, columns=normal_columns)
    all_deals.fillna(value='', inplace=True)
    all_deals['dealId']             = all_deals['dealId'].astype(dtype=int)
    all_deals['isDeleted']          = all_deals['isDeleted'].astype(dtype=bool)
    all_deals['dealname']           = all_deals['dealname'].astype(dtype=object)
    all_deals['description']        = all_deals['description']
    all_deals['design_date']        = pd.to_datetime(all_deals['design_date'], unit='ms')
    all_deals['closedate']          = pd.to_datetime(all_deals['closedate'], unit='ms')
    all_deals['amount']             = pd.to_numeric(all_deals['amount'])
    all_deals['pipeline']           = all_deals['pipeline'].astype(dtype=object)
    all_deals['dealstage']          = all_deals['dealstage'].astype(dtype=object)
    all_deals['permit_issue_date']  = pd.to_datetime(all_deals['permit_issue_date'])
    all_deals['permit_']            = all_deals['permit_'].astype(dtype=object)
    all_deals['permit']             = all_deals['permit'].astype(dtype=object)
    all_deals['permit_type']        = all_deals['permit_type'].astype(dtype=object)
    all_deals['work_descrption']    = all_deals['work_descrption'].astype(dtype=object)
    all_deals['last_inspection']    = all_deals['last_inspection'].astype(dtype=object)
    all_deals['last_inspection_date'] = pd.to_datetime(all_deals['last_inspection_date'], unit='ms')
    all_deals['insp_n']             = all_deals['insp_n'].astype(dtype=object)
    all_deals['insp_note']          = all_deals['insp_note'].astype(dtype=object)

    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    all_deals.to_sql(name=sorting.DEALS_TABLE, con=conn, if_exists='replace', index=False)

    with open(downuploaded_deals, 'w') as f:
        f_csv = csv.DictWriter(f, all_columns)
        f_csv.writeheader()
        f_csv.writerows(all_deals_cdr)
    return


if __name__ == '__main__':
    main()
    print('main - done')
