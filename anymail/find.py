"""
take a website name, split it and make an async request, searching
for all the emails in the domain.
"""
import csv
from os import environ
from sys import exit
import time
from collections import OrderedDict
import requests


def emails(domain):
    # should be excluded
    # wordpress.com, houzz.com, yelp.com, facebook.com

    # initiate the big objects
    rows = []
    fieldnames = ['Name', 'Phone Mobile', 'Phone Voip', 'Phone Toll',
                  'Phone Landline', 'Phone Unknown', 'Contact Person',
                  'Address', 'City', 'Zipcode', 'State', 'Category',
                  'Website', 'Facebook', 'Twitter', 'Google',
                  'Linkedin', 'emails', 'email_class']


    with open(file_path) as f:
        f_csv = csv.DictReader(f, restkey='Rest', restval='')
        with open(output_file_path, 'w') as wr:
            wr_csv = csv.DictWriter(wr, fieldnames=fieldnames)
            wr_csv.writeheader()
            for row in f_csv:
                website = row['Website']
                if not website:  # check whether there is a website
                    pass
                else:

                wr_csv.writerow(row)
                rows.append(row)

    with open(final_file_path,'w') as f:
        f_csv = csv.DictWriter(f, fieldnames=fieldnames)
        f_csv.writeheader()
        f_csv.writerows(rows)

    print('OK')
    return


def main():
    pass