# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
from random import randint
import hubspot


def main():
    conn_source = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)
    companies_with_emails = pd.read_sql_table(
        table_name=sorting.FOUND_EMAILS_TABLE, con=conn_source)

    conn_reference = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_result = sqlalc.create_engine(sorting.LOG_DATABASE_URI)

    existing_contacts = pd.read_sql_table(
        table_name=sorting.CONTACTS_EVERYTHING_TABLE, con=conn_reference)
    known_contacts = set(existing_contacts['email'])
    del existing_contacts

    contact_template = {'firstname': '', 'lastname': '',
                        'company': '', 'company_index': '',
                        'jobtitle': ''}

    # connection data
    connection_template = {'fromObjectId': '', 'toObjectId': '',
                           'category': 'HUBSPOT_DEFINED', 'definitionId': 2}

    start_company = 0
    for indx, company in companies_with_emails.iterrows():
        if indx >= start_company:
            con_cre_list = []
            companyId       = company['companyId']
            company_name    = company['name']
            list_of_emails  = company['emails'].split(' ')
            for ind, e_mail in enumerate(list_of_emails):
                if e_mail not in known_contacts:
                    row = {}
                    row.update({'companyId': companyId,
                                'email': e_mail})
                    parameters = contact_template.copy()
                    first_name, rest = e_mail.split('@')
                    parameters['firstname'] = first_name.title()
                    last, _ = rest.split('.')
                    parameters['lastname'] = last.title()
                    if first_name.startswith('info'):
                        parameters['company_index'] = '0'
                    else:
                        parameters['company_index'] = str(ind + 1)
                    parameters['company'] = company_name
                    result = hubspot.contacts.create_or_update_contact(e_mail, parameters)
                    if result:
                        vid = result['vid']
                        row.update({'vid': vid})
                        connected = hubspot.associations.create_association_of_objects(
                            from_object_id=companyId, to_object_id=vid,
                            association_type='2')
                        if connected:
                            row['connected'] = True
                        else:
                            row['connected'] = False
                    else:
                        print('Failed to create a contact for email ', e_mail)
                        row['vid'] = ''
                        row['connected'] = False
                    row.update(parameters)
                    con_cre_list.append(row)
                else:
                    print('There is a contact with email ', e_mail, ' in the system.')
            contacts_created = pd.DataFrame(con_cre_list)
            contacts_created.to_sql(name=sorting.CREATED_CONTACTS_TABLE,
                                    con=conn_result, if_exists='append', index=False)
        else:
            pass
    return


if __name__ == '__main__':
    main()
    print('main - done')
