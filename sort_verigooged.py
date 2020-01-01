# -*- coding: utf-8 -*-
"""...
"""
import sorting
import sqlalchemy as sqlalc
import pandas as pd


def main():
    conn_reference = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)
    verigoog = pd.read_sql_table(
        table_name=sorting.VERIGOOG_CONTRACTORS_TABLE, con=conn_reference)

    print('ok')
    return


if __name__ == '__main__':
    main()
    print('done')