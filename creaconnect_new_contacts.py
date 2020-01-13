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
                        'jobtitle': 'General Contractor employee'}

    # connection data
    connection_template = {'fromObjectId': '', 'toObjectId': '',
                           'category': 'HUBSPOT_DEFINED', 'definitionId': 2}

    start_company = 0
    for indx, company in companies_with_emails.iterrows():
        if indx >= start_company:
            con_cre_list = []
            companyId       = company['companyId']
            list_of_emails  = company['emails'].split(' ')
            for ind, e_mail in enumerate(list_of_emails):
                if e_mail not in known_contacts:
                    row = {}
                    row.update({'companyId': companyId})
                    parameters = contact_template.copy()
                    first_name, _ = e_mail.split('@')
                    parameters['lastname'] = 'Auto_' + str(randint(1, 999999))
                    if first_name.startswith('info'):
                        parameters['company_index'] = '0'
                    else:
                        parameters['company_index'] = str(ind + 1)
                    parameters['firstname'] = first_name
                    parameters['company'] = company['name']
                    result = hubspot.contacts.create_or_update_contact(e_mail, parameters)
                    if result:
                        vid = result['vid']
                        row['vid'] = vid
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
                    con_cre_list.append(row)
                else:
                    print('There is a contact with email ', e_mail, ' in the system.')
            contacts_created = pd.DataFrame()
            contacts_created.to_sql(name=sorting.CREATED_CONTACTS_TABLE,
                                    con=conn_result, if_exists='append', index=False)
        else:
            pass
    return


if __name__ == '__main__':
    main()
    print('main - done')


import requests
import os
import csv
from collections import OrderedDict


API_KEY = os.environ['API_KEY']
CONTACT_CREATE_OR_UPDATE_URL = 'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/'
CONNECTION_CREATE_URL = 'https://api.hubapi.com/crm-associations/v1/associations'
companies_created_with_emails_path = '/media/alxfed/toca/aa-crm/int-desanddec/upload/int_designers_created_with_emails.csv'
contacts_created_path = '/media/alxfed/toca/aa-crm/int-desanddec/upload/int_designers_contacts_created.csv'

headers = {"Content-Type": "application/json"}
querystring = {"hapikey": API_KEY}

input_columns = ['Name', 'Type', 'Phone Number', 'Phone Contact', 'Phone Mobile',
                 'Phone Voip', 'Phone Toll', 'Phone Landline',
                 'Phone Unknown', 'Address', 'City',
                 'Zipcode', 'State', 'Category', 'Website',
                 'Facebook', 'Twitter', 'Google', 'Linkedin',
                 'companyId', 'emails']

# contact create request data
data = {'properties':
    [
        {
          "property": "firstname",
          "value": ""
        },
        {
          "property": "lastname",
          "value": ""
        },
        {
          "property": "company",
          "value": ""
        },
        {
          "property": "jobtitle",
          "value": "Interior Designer & Decorator employee"
        }
    ]
}

# connection data

connection_data = {
  "fromObjectId": '',
  "toObjectId": '',
  "category": "HUBSPOT_DEFINED",
  "definitionId": 2
}

# output
output_rows = []
output_columns = ['Name', 'companyId', 'firstname', 'lastname', 'email', 'vid', 'connected']
enu = 11210


with open(companies_created_with_emails_path) as f:
    f_csv = csv.DictReader(f, restkey='Rest', restval='')
    for row in f_csv:
        output_row = OrderedDict()
        output_row['Name'] = row['Name']
        companyId = row['companyId']
        output_row['companyId'] = companyId
        list_of_emails = row['emails'].split(' ')
        for email in list_of_emails:
            name, _ = email.split('@')
            lastname = 'Auto_' + str(enu+1)
            enu += 1
            output_row['firstname'] = name
            output_row['lastname'] = lastname
            output_row['email'] = email
            data['properties'][0]['value'] = name
            data['properties'][1]['value'] = lastname
            data['properties'][2]['value'] = row['Name']
            req_url = '{}{}/'.format(CONTACT_CREATE_OR_UPDATE_URL, email)
            response = requests.request("POST", url=req_url, json=data,
                                        headers=headers, params=querystring)
            if response.status_code == 200:
                vid = response.json()['vid']
                output_row['vid'] = vid
                connection_data['fromObjectId'] = companyId
                connection_data['toObjectId'] = vid
                resp = requests.request("PUT", url=CONNECTION_CREATE_URL, json=connection_data,
                                        headers=headers, params=querystring)
                if resp.status_code == 204:
                    output_row['connected'] = True
                else:
                    output_row['connected'] = False
            else:
                output_row['vid'] = ''
                output_row['connected'] = False
            output_rows.append(output_row)
            print(output_row, resp.status_code)

with open(contacts_created_path,'w') as f:
    f_csv = csv.DictWriter(f, output_columns)
    f_csv.writeheader()
    f_csv.writerows(output_rows)

print('Big OK')