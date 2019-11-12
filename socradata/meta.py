# -*- coding: utf-8 -*-
""" Reading a catalog for a URI and metadata for particular dataset
"""
from .constants import *
from requests import Request, Session, get
from datetime import datetime


class dataset_meta(object): # initialize with four_by_four
    def __init__(self, four_by_four):
        params = {'ids': four_by_four}
        response = get(url=DISCOVERY_API_URL, params=params)
        resource = response.json()['results'][0]['resource']
        self.id = resource['id']
        self.name = resource["name"]
        update = resource['data_updated_at']
        self.updated = datetime.strptime(update, '%Y-%m-%dT%H:%M:%S.000Z')
        self.columns_names = resource["columns_name"]
        self.column_fields_names = resource["columns_field_name"]
        self.columns_data_types = resource['columns_datatype']


def all_chicago_datasets():
    session = Session()
    # both, the domain and the context should be the same URI here
    params = {'domains': 'data.cityofchicago.org', 'search_context': 'data.cityofchicago.org'}
    request = Request(method='GET', url=DISCOVERY_API_URL, params=params)
    prepped = request.prepare()
    response = session.send(prepped)
    return response.json()['results']


def metadata_for_dataset(four_by_four):
    params = {'ids': four_by_four}
    response = get(url=DISCOVERY_API_URL, params=params)
    resource = response.json()['results'][0]['resource']
    metadata = {}
    metadata.id = resource['id']
    metadata.name = resource["name"]
    update = resource['data_updated_at']
    metadata.updated = datetime.strptime(update, '%Y-%m-%dT%H:%M:%S.000Z')
    metadata.columns_names = resource["columns_name"]
    metadata.column_fields_names = resource["columns_field_name"]
    metadata.columns_data_types = resource['columns_datatype']
    return metadata


def main():
    print('The meta.py has been launched as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')