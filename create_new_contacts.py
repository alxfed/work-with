# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting

import requests
import os
import csv
from collections import OrderedDict
from random import randint


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

    param_template = {'firstname': '', 'lastname': '',
                      'company': '', 'company_index': '',
                      'jobtitle': 'General Contractor employee'}
    parameters = param_template.copy()

    contacts_created = pd.DataFrame()
    contacts_created.to_sql(name=sorting.CREATED_CONTACTS_TABLE,
                            con=conn_result, if_exists='append', index=False)

    return


if __name__ == '__main__':
    main()
    print('main - done')


input_columns = ['Name', 'Type', 'Phone Number', 'Phone Mobile',
                 'Phone VoIP', 'Phone Toll', 'Phone Landline',
                 'Phone Unidentified', 'Address', 'City',
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
          "property": "company_index",
          "value": ""
        },
        {
          "property": "jobtitle",
          "value": "Kitchen & Bath Designer employee"
        }
    ]
}


# output
output_rows = []
output_columns = ['Name', 'companyId', 'firstname', 'lastname', 'email', 'vid']


with open(companies_created_with_emails_path) as f:
    f_csv = csv.DictReader(f, restkey='Rest', restval='')
    for row in f_csv:
        output_row = OrderedDict()
        output_row['Name'] = row['Name']
        output_row['companyId'] = row['companyId']
        list_of_emails = row['emails'].split(' ')
        for index, email in enumerate(list_of_emails):
            if email in known_contacts:
                name, _ = email.split('@')
                lastname = 'Auto_' + str(randint(1, 999999))
                output_row['firstname'] = name
                output_row['lastname'] = lastname
                output_row['email'] = email
                data['properties'][0]['value'] = name
                data['properties'][1]['value'] = lastname
                data['properties'][2]['value'] = row['Name']
                if name.startswith('info'):
                    ind = '0'
                else:
                    ind = str(index+1)
                data['properties'][3]['value'] = ind
                req_url = '{}{}/'.format(CONTACT_CREATE_OR_UPDATE_URL, email)
                response = requests.request("POST", url=req_url, json=data,
                                            headers=headers, params=querystring)
                if response.status_code == 200:
                    output_row['vid'] = response.json()['vid']
                else:
                    output_row['vid'] = ''
                output_rows.append(output_row)
                print(output_row, response.status_code)
            else:
                pass


with open(contacts_created_path,'w') as f:
    f_csv = csv.DictWriter(f, output_columns)
    f_csv.writeheader()
    f_csv.writerows(output_rows)

print('ok')