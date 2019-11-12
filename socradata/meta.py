# -*- coding: utf-8 -*-
"""...
"""
from .constants import *
from requests import Request, Session, get


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
    return response.json()['results']

def main():
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')