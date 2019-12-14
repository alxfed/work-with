# -*- coding: utf-8 -*-
"""https://jsonlines.readthedocs.io/en/latest/
"""
import jsonlines
import pandas as pd
import hubspot
import datetime as dt
from tabulate import tabulate


def main():
    # permit, dealId, (note) id
    ownerId = 40202623  # Data Robot
    dealId =

    # deals_with_permits = all_deals[all_deals['permit_'].notnull()]
    for index, note in created_notes.iterrows():
        dealId = note['dealId']
        insp_n = note['insp_n']
        last_inspection_date = note['insp_date']
        last_inspection = note['insp_type']
        insp_note = note['id']
        result = hubspot.deals.update_a_deal_oauth(dealId, {'last_inspection': last_inspection,
                                                            'last_inspection_date': last_inspection_date,
                                                            'insp_n': insp_n,
                                                            'insp_note': insp_note})
        if result:
            print('Updated deal #  ', dealId)
    return


if __name__ == '__main__':
    main()
    print('main - done')