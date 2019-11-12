# -*- coding: utf-8 -*-
"""https://dev.socrata.com/foundry/data.cityofchicago.org/r5kz-chrr
"""
import datetime as dt
import requests
import pandas as pd
from os import environ


RESOURCE_URL = 'data.cityofchicago.org'
RESOURCE_ID  = 'r5kz-chrr'                      # licenses data
api_token = environ['API_TOKEN']
api_url = f'https://{RESOURCE_URL}/resource/{RESOURCE_ID}.json'
header = {'Content-Type': 'application/json', 'X-App-Token': api_token}


def data_chunk(uri):
    response = requests.get(uri, headers=header)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 201:
        raise RuntimeError("Request Processing")
    elif response.status_code == 400:
        raise RuntimeError("Bad Request")
    elif response.status_code == 401:
        raise RuntimeError("Unauthorized")
    elif response.status_code == 403:
        raise RuntimeError("Forbidden")
    elif response.status_code == 404:
        raise RuntimeError("Not Found")
    elif response.status_code == 429:
        raise RuntimeError("Too many Requests")
    elif response.status_code == 500:
        raise RuntimeError("Server Error")
    else:
        return None # silently return nothing


def main():
    """Read a chunk with date_issued in predefined window
    """
    unlicensed_gen_contractors_file = '/home/alxfed/archive/unlicensed_contractors_with_permits.csv'
    contractors = pd.read_csv(unlicensed_gen_contractors_file, dtype=object)

    data = pd.DataFrame()

    # dates if necessary
    start_dt = dt.datetime(year=2017, month=1, day=1, hour=0, minute=0, second=0)
    start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%S')
    end_dt = dt.datetime(year=2019, month=11, day=4, hour=0, minute=0, second=0)
    end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%S')
    # api_call = api_url + f'?$where=license_start_date between "{start_str}" and "{end_str}"'

    # license_status=AAI , expiration_date=
    # api_call = api_url + '?license_status=AAI' + f'&$q={full_text_query_string}' #  + ' AND ' + ''

    for index, contractor in contractors.iterrows():
        like = contractor['name']
        likeness, sep, rest = like.partition(' ')
        api_call = api_url + f"?$where=legal_name like '%25{rest}%25'" # here %25 are URL encoded symbol '%' standing for any number of any characters
        found = pd.DataFrame.from_records(data_chunk(api_call))
        if found.empty:
            print('Not found ', likeness)
        else:
            data = data.append(found, sort=False, ignore_index=True)
            print('Added found for ', likeness)
    data.to_csv('/media/alxfed/archive/found_licenses.csv', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')


'''
# long complex request

api_request = f'{api_url}?${requ}={argu}'

# but if the parameters of the query are already in a dictionary
# then the trick is:

person = {'name': 'Alex', 'age': 64}
message = "Hello, {name}. You are {age}.".format(**person)
'''