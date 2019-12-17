# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import hubspot
import sorting
import sqlalchemy as sqlalc


def main():
    properties = {
        'dealname': '',
        'dealtype':'newbusiness',
        'general_contractor':'',
        'amount': '',
        'work_descrption': '',
        'pipeline': '815585',
        'dealstage':'815586',
        'permit_':'',
        'permit_issue_date': '',
        'permit_type': '',
        'closedate':'' # ,
        # 'hs_analytics_source_data_1':'',
        # 'hs_analytics_source_data_2':'',
    }
    associations= {
        'associatedCompanyIds': [],
        'associatedVids': [],
        'associatedDealIds': [],
        'associatedTicketIds': []
    }

    conn_source = sqlalc.create_engine(sorting.PREP_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.OLD_COMPANIES_PERMITS_TABLE, con=conn_source)

    created = pd.DataFrame()
    not_created = pd.DataFrame()
    for indx, deal in deals.iterrows():
        permit_type = ''
        line = pd.Series()
        prop = properties.copy()
        asso = associations.copy()
        asso['associatedCompanyIds'] = [deal['companyId']]
        permit_t = deal['permit_type']
        if permit_t == 'PERMIT - RENOVATION/ALTERATION':
            permit_type = 'RA '
        elif permit_t == 'PERMIT - NEW CONSTRUCTION':
            permit_type = 'NC '
        else:
            print('Some other permit type here, not NC and not RA')
        deal_name = str(deal['street_number']) + ' ' + str(deal['street_direction']) + ' '
        deal_name = deal_name + str(deal['street_name']) + ' ' + str(deal['suffix'])
        deal_name = permit_type + deal_name.title()
        prop['dealname'] = deal_name
        prop['general_contractor'] = deal['name'].title()
        prop['amount'] = .15 * float(deal['reported_cost'])
        prop['work_descrption'] = deal['work_description']
        prop['permit_'] = deal['permit_']
        prop['permit_type'] = deal['permit_type']
        prop['permit_issue_date'] = deal['issue_date'].strftime('%Y-%m-%d')
        close_date = int(deal['issue_date'].value / 1000000)
        prop['closedate'] = close_date
        crea = hubspot.deals.create_a_deal_oauth(prop, asso)
        if crea:
            line['dealId'] = str(int(crea['dealId']))
            line['isDeleted'] = str(bool(crea['isDeleted']))
            line = line.append(deal)
            created = created.append(line, ignore_index=True)
        else:
            not_created = not_created.append(deal, ignore_index=True)

    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    # the ids are in FLOAT format if you don't do something right here
    created.to_sql(
        name=sorting.CREATED_DEALS_TABLE,
        con=conn_result, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')
