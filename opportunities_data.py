# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
from numpy import nan


def main():
    input_file_path = '/media/alxfed/toca/presentation/gen_contractors_new_permits.csv'
    reference_file_path = '/media/alxfed/toca/presentation/unique_gen_contractors.csv'

    origin      = pd.read_csv(input_file_path)
    reference   = pd.read_csv(reference_file_path)

    big_permits = origin[(origin['reported_cost'] > 100000) &
                         ((origin['permit_type'] == 'PERMIT - NEW CONSTRUCTION') |
                          (origin['permit_type'] == 'PERMIT - RENOVATION/ALTERATION'))]

    # grouped = pd.DataFrame()
    # grouped[['general_contractor', 'total']] = big_permits['reported_cost'].groupby(big_permits['general_contractor']).sum()

    sorted_big_permits = big_permits.sort_values(by=['general_contractor', 'issue_date'])
    # output = sorted_big_permits.set_index('general_contractor')

    pivot = sorted_big_permits.pivot_table(index=['general_contractor',
                                                  pd.Grouper(key='issue_date', freq='M')],
                                           values=['reported_cost'], aggfunc='sum')
    
    pivot.to_csv('/media/alxfed/toca/presentation/pivot_by_gen_contractors.csv')
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')