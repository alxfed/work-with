# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd


def main():
    duta = pd.DataFrame({'a': [1, 2, 3],
                         'b': [4, 5, 6],
                         'c': [7, 8, 9]})
    data = pd.DataFrame([{'d': 11, 'e': 12, 'f': 13},
                         {'d': 14, 'e': 15, 'f': 16},
                         {'d': 17, 'e': 18, 'f': 19}])
    on_auto_key = duta.join(data)
    duta.index = ['ru', 'mu', 'bu']
    on_index_with_sorting = duta.join(data, how='outer')
    print(duta)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')