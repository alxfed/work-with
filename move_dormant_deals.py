# -*- coding: utf-8 -*-
"""https://www.chicago.gov/city/en/depts/bldgs/provdrs/gen_contract.html
"""
import pandas as pd
import hubspot
import sqlalchemy as sqlalc
import sorting
from itertools import chain, islice


def chunks(n, iterable):
    iterable = iter(iterable)
    while True:
        yield chain([next(iterable)], islice(iterable, n - 1))

def main():
    # all deals from HubSpot
    conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.THOSE_DEALS_TABLE, con=conn)

    # Sales Pipeline =
    pipeline = '1243605'
    # Follow-up on Quote =
    dealstage_dormant = '1243606'


    deals_list = deals['dealId'].to_list()

    # for indx, row in no_close_date_follow_up.iterrows():
    #     line = {}
    #     deal_properties = hubspot.deals.get_a_deal(row['dealId'])['properties']
    #     source = deal_properties['dealstage']['source']
    #     if deal_properties['dealstage']['source'] == 'BATCH_UPDATE':
    #         # print('here you are') # 155182970482
    #         sing = deal_properties['dealstage']['timestamp']
    #         dif = abs(sing - hs_date)
    #         if dif < 10000000:
    #             line['dealId'] = row['dealId']
    #             line['timestamp'] = str(sing)
    #             datm = pd.to_datetime(sing, unit='ms')
    #             print("deal is", row['dealId'], "  this timestamp is:", datm)
    #             line_list.append(line)
    #
    # those_deals = pd.DataFrame(line_list)
    # # conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    # those_deals.to_sql(name=sorting.THOSE_DEALS_TABLE, con=conn, if_exists='replace', index=False)
    params = {'pipeline': '1243605', 'dealstage': '1243606'}
    chunk_length = 100
    chunk_list = [deals_list[i:i + chunk_length] for i in range(0, len(deals_list), chunk_length)]
    it = 0
    for chunk in chunk_list:
        response = hubspot.deals.batch_update_deals(chunk, params)
        it += 1
        print('Updated', it)
    print('ok')

    return


if __name__ == '__main__':
    main()
    print('main - done')
