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
    row = {}

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
            response = requests.request('POST', api_url,
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
            row.update({'name': name})
            row.update({'domain': domain})
            row.update({'emails': " ".join(resp['emails'])})
            row.update({'email_class': resp['email_class']})
            print(row['name'], row['domain'], row['emails'], row['email_class'])
            return row
        else:
            print(name, 'Timeout')
    else:
        print('I dunno what this is...', response.status_code)
        pass
    return


def main():
    pass