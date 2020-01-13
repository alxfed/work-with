# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd


def main():
    param_template = {'firstname': '', 'lastname': '',
                      'company': '', 'company_index': '',
                      'jobtitle': ''}

    return


if __name__ == '__main__':
    main()
    print('main - done')

import requests
import os
import csv
from collections import OrderedDict
from random import randint
import pandas as pd


API_KEY = os.environ['API_KEY']
CONTACT_CREATE_OR_UPDATE_URL = 'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/'
companies_created_with_emails_path = '/media/alxfed/toca/aa-crm/kb-designers/upload/kitchen_and_bath_designers_created_with_emails.csv'
existing_contacts_path = '/media/alxfed/toca/aa-crm/work/all-contacts.csv'
contacts_created_path = '/media/alxfed/toca/aa-crm/kb-designers/upload/kitchen_and_bath_designers_contacts_created_with_index.csv'

# emails are in the 'Email' column of contacts file
existing_contacts = pd.read_csv(existing_contacts_path)
known_contacts = set(existing_contacts['Email'])


headers = {"Content-Type": "application/json"}
querystring = {"hapikey": API_KEY}

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