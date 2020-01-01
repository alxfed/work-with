# -*- coding: utf-8 -*-
"""...
"""
from tldextract import extract
import pandas as pd
import sqlalchemy as sqlalc
import sorting


def domain_and_website(row):
    website = row['website']
    domain = row['domain']
    if website:
        tsd1, td1, tsu1 = extract(website)  # tldextract
        domain = td1 + '.' + tsu1
        website = website
    elif domain:
        tsd2, td2, tsu2 = extract(domain)

    return pd.Series([])


def main():
    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_reference)

    output = pd.DataFrame()
    output['companyId'] = companies['companyId']
    output['idDeleted'] = companies['idDeleted']
    output['name'] = companies['name']
    output['phone'] = companies['phone']
    output['address'] = companies['address']
    output['city'] = companies['city']
    output['zip'] = companies['zip']
    output['state'] = companies['state']
    output['category'] = companies['category']
    output[['domain', 'website']] = companies.apply(domain_and_website, axis=1)
    output['summary_note_number'] = companies['summary_note_number']
    output['summary_note_date_str'] = companies['summary_note_date_str']

    return


if __name__ == '__main__':
    main()
    print('main - done')