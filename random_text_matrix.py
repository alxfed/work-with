# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import numpy as np
import string


def work_on_rows(row, ref, sta):
    d = ''; e = ''; f = ''
    if row['name'] in ref['name'].values:
        d = row['name']
    if row['address'] in sta['name'].values:
        e = sta['address']
    if row['phone'] in sta['phone'].values:
        f = row['phone']
    return pd.Series([d, e, f])


def main():
    lett = list(string.ascii_lowercase)
    df = pd.DataFrame(np.random.choice(lett, size=(3, 3)), index=['a', 'b', 'c'], columns=[0, 1, 2])
    reference = pd.DataFrame(np.random.choice(lett, size=(4, 3)), columns=['name', 'address', 'phone'])
    state = pd.DataFrame(np.random.choice(lett, size=(5, 3)), columns=['name', 'address', 'phone'])

    out = pd.DataFrame()
    out = df.append(reference, ignore_index=True)
    df.append(state)
    #out[['D', 'E', 'F']] = df.apply(work_on_rows, axis=1, ref=reference, sta=state)
    print(out)
    return


if __name__ == '__main__':
    main()
    print('main - done')