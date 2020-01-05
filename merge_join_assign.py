# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd


def other_columns(row, a, b):
    e = a * row['a']
    f = b * row['a']
    return pd.Series([e, f])


def main():
    duta = pd.DataFrame({'a': [1, 2, 3],
                         'b': [4, 5, 6],
                         'c': [7, 8, 9]}, index=[1,2,3])
    data = pd.DataFrame([{'d': 11, 'e': 12, 'f': 13},
                         {'d': 14, 'e': 15, 'f': 16},
                         {'d': 17, 'e': 18, 'f': 19}])
    on_auto_key = duta.join(data) # left join
    # duta.index = ['ru', 'mu', 'bu']
    on_auto_key = duta.join(data, how='outer')
    on_index_with_sorting = duta.join(data, how='outer')
    data = data.assign(a=lambda x: x.d - 10)

    shmuta = pd.DataFrame()
    shmuta[['a', 'b']] = duta.apply(other_columns, axis=1, a=1, b=2)
    merged_on_column = pd.merge(duta, data, how='outer')
    print(duta)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')