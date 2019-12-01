# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import csv
import sqlalchemy as sqlalc
import numpy as np


def main():
    # all deals from HubSpot
    # Production = 7f8ad520-75d7-4f9f-b655-4fab5439aed5
    # Quotes = dd6958f7-3696-4de5-a95e-77d3a68aed44
    # Sales = default
    # New Construction/Renovation/Alteration = 815585
    downuploaded_deals = '/home/alxfed/archive/deals_database_everything.csv'
    deal_properties_table_url = '/home/alxfed/archive/deal_properties_table.csv'

    request_params = []
    normal_columns = ['dealId', 'isDeleted']
    deal_properties_columns = ['name', 'label', 'description']
    include_associations = True

    all_props_json = hubspot.deals.get_all_deal_properties()
    all_props_table = []
    line = dict()
    for prop in all_props_json:
        name = prop['name']
        request_params.append(name)
        normal_columns.append(name)
        line['name'] = name
        line['label'] = prop['label']
        line['description'] = prop['description']
        all_props_table.append(line)

    deal_properties_table = pd.DataFrame(all_props_table, columns=deal_properties_columns)
    deal_properties_table.to_csv(deal_properties_table_url, index=False)

    all_deals_cdr, all_columns = hubspot.deals.get_all_deals_oauth(request_params, include_associations)
    all_deals = pd.DataFrame(all_deals_cdr, columns=normal_columns)
    all_deals.fillna(value='', inplace=True)
    all_deals['dealId'] = all_deals['dealId'].astype(dtype=int)
    all_deals['isDeleted'] = all_deals['isDeleted'].astype(dtype=bool)
    all_deals['design_date'] = pd.to_datetime(all_deals['design_date'], unit='ms')
    all_deals['closedate'] = pd.to_datetime(all_deals['closedate'], unit='ms')
    all_deals['amount'] = pd.to_numeric(all_deals['amount'])
    all_deals['pipeline'] = all_deals['pipeline'].astype(dtype=object)
    all_deals['dealstage'] = all_deals['dealstage'].astype(dtype=object)
    all_deals['permit_issue_date'] = pd.to_datetime(all_deals['permit_issue_date'])
    all_deals['last_inspection_date'] = pd.to_datetime(all_deals['last_inspection_date'], unit='ms')

    conn = sqlalc.create_engine('sqlite:////home/alxfed/dbase/home.sqlite')
    all_deals.to_sql(name='deals_everything', con=conn, if_exists='replace', index=False)

    with open(downuploaded_deals, 'w') as f:
        f_csv = csv.DictWriter(f, all_columns)
        f_csv.writeheader()
        f_csv.writerows(all_deals_cdr)
    return


if __name__ == '__main__':
    main()
    print('main - done')
