# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sorting
import sqlalchemy as sqlalc


def main():
    # read the downuploaded table of new_permits
    conn = sqlalc.create_engine(sorting.SOURCE_DATABASE_URI)
    data = pd.read_sql_table(table_name='new_permits', con=conn)
    return


if __name__ == '__main__':
    main()
    print('main - done')