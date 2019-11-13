"""
take a website name, split it and make an async request, searching
for all the emails in the domain.
"""
from .constants import *
import time
from collections import OrderedDict
import requests


def emails(name, domain):
    # should be excluded
    # wordpress.com, houzz.com, yelp.com, facebook.com

    # initiate the big objects
    rows = []
    fieldnames = ['Name', 'Phone Mobile', 'Phone Voip', 'Phone Toll',
                  'Phone Landline', 'Phone Unknown', 'Contact Person',
                  'Address', 'City', 'Zipcode', 'State', 'Category',
                  'Website', 'Facebook', 'Twitter', 'Google',
                  'Linkedin', 'emails', 'email_class']

    payload = {'domain': domain, 'company_name': name}
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)

    if response.status_code > 202:
        """errors
        """
        whats_up = response.json()
        print('Wow! Errors happen!', response.status_code, whats_up['error'])
        pass
    elif response.status_code < 203:
        timeout = False
        attempts = 0
        while response.status_code != 200:
            time.sleep(3)
            r = requests.request('POST', api_url,
                                 headers=headers, json=payload)
            if response.status_code == 200:
                break
            else:
                attempts += 1
                print(attempts)
                if attempts > 10:
                    timeout = True
                    break
        if not timeout:
            resp = response.json()
            row.update({'emails': " ".join(resp['emails'])})
            row.update({'email_class': resp['email_class']})
            print(row['Name'], row['emails'], row['email_class'])
        else:
            print(row['Name'], 'Timeout')
    else:
        print('I dunno what this is...', response.status_code)
        pass
    return


def main():
    pass