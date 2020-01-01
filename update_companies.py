# -*- coding: utf-8 -*-
"""...
"""
from tldextract import extract
import pandas as pd
import sqlalchemy as sqlalc
import sorting


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)

    tsd, td, tsu = extract(companies['website'])  # tldextract
    domain = td + '.' + tsu
    return


if __name__ == '__main__':
    main()
    print('main - done')