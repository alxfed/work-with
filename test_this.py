# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy as sqlalc
import pandas as pd
import sorting


def main():
    df = [
        {'day': 'wed', 'exists': True, 'name': 'First Data Corporation',    'number': 135},
        {'day': 'mon', 'exists': True, 'name': 'Second Data Corp.',         'number': 246},
        {'day': 'sat', 'exists': True, 'name': 'Mk Builders, Inc.',         'number': 247},
        {'day': 'thu', 'exists': True, 'name': 'Data Construction, LLC',    'number': 762}
    ]
    data = pd.DataFrame(df)
    substring = 'Data'
    a = data[data['name'].str.contains(substring)]
    return


if __name__ == '__main__':
    main()
    print('main - done')