# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy
import pandas as pd


def filter_out_known_companies(data):
    new = pd.DataFrame()
    old = pd.DataFrame()
    return new, old


def filter_out_big_ra_and_nce(data):
    big_nc = pd.DataFrame()
    big_ra = pd.DataFrame()
    return big_nc, big_ra


def extract_general_contractors_out_of_new_permits(data):
    output_list = []
    for row_n, row in data.iterrows():
        if row['reported_cost'] > 100000:
            for n in range(14):
                contact_number = str(n + 1)
                con_type_key = f'contact_{contact_number}_type'
                if con_type_key in row.keys():
                    contact_type = row[con_type_key]
                    if contact_type == 'CONTRACTOR-GENERAL CONTRACTOR':
                        line = {'name':     row[f'contact_{contact_number}_name'],
                                'city':     row[f'contact_{contact_number}_city'],
                                'state':    row[f'contact_{contact_number}_state'],
                                'zip':      row[f'contact_{contact_number}_zipcode'],
                                'permit_':  row['permit_']
                                }
                        output_list.append(line)
                        print(line)
                else:
                    break

    general_contractors = pd.DataFrame(output_list)
    return general_contractors


def main():
    print('You have launched companies.py as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')