# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import sqlalchemy as sqlalc
import sorting
from time import sleep


def main():
    # all deals from HubSpot
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.DEALS_TABLE, con=conn)

    # Sales Pipeline =
    pipeline = 'default'
    # Follow-up on Quote =
    dealstage_followup = '2cd78f67-7bfe-4691-824f-24dd4d33aff2'
    # date March 3 2019
    hs_date = 1551829704821

    follow_up = deals[deals['dealstage'] == dealstage_followup]
    no_close_date_follow_up = follow_up[follow_up.closedate.isnull()]

    line_list = []

    for indx, row in no_close_date_follow_up.iterrows():
        line = {}
        deal_properties = hubspot.deals.get_a_deal(row['dealId'])['properties']
        source = deal_properties['dealstage']['source']
        if deal_properties['dealstage']['source'] == 'BATCH_UPDATE':
            # print('here you are') # 155182970482
            sing = deal_properties['dealstage']['timestamp']
            dif = abs(sing - hs_date)
            if dif < 10000000:
                line['dealId'] = row['dealId']
                line['timestamp'] = str(sing)
                datm = pd.to_datetime(sing, unit='ms')
                print("deal is", row['dealId'], "  this timestamp is:", datm)
                line_list.append(line)

    those_deals = pd.DataFrame(line_list)
    # conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    those_deals.to_sql(name=sorting.THOSE_DEALS_TABLE, con=conn, if_exists='replace', index=False)
    print('ok')
    
    return


if __name__ == '__main__':
    main()
    print('main - done')
