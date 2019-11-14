# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants


def create_static_list(name):
    listId = ''
    response = requests.request(method='POST', url=constants.LISTS_ALL_URL,
                                json={"name":name},
                                headers=constants.authorization_header)
    if response.status_code == 200:
        res = response.json()
        listId = res['listId']
    return listId


def get_all_lists_oauth():
    # prepare for the inevitable output
    all_lists    = []
    # prepare for the pagination
    has_more = True
    offset = 0
    count = 250  # max 250
    # what is being returned
    output_columns = ["dynamic", "metaData", 
                      "name", "filters", "createdAt", "listId", "updatedAt",
                      "listType", "internalListId", "deleteable"]
    # Now the main cycle
    while has_more:
        response = requests.get(url=constants.LISTS_ALL_URL,
                                headers=constants.authorization_header,
                                params={'count':count, 'offset': offset})
        if response.status_code == 200:
            res = response.json()
            has_more    = res['has-more']
            offset      = res['offset']
            lists       = res['lists']
            all_lists.extend(lists)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_lists, output_columns


def get_all_contacts_in(listId):
    # https://api.hubapi.com/contacts/v1/lists/226468/contacts/all
    # prepare for the inevitable output
    all_list = []
    # prepare for the pagination
    has_more = True
    offset = 0
    count = 250  # max 250
    # what is being returned
    output_columns = ["dynamic", "metaData",
                      "name", "filters", "createdAt", "listId", "updatedAt",
                      "listType", "internalListId", "deleteable"]
    # Now the main cycle
    req_url = constants.LISTS_ALL_URL + '/'+ listId + '/contacts/all'
    while has_more:
        response = requests.get(url=req_url,
                                headers=constants.authorization_header,
                                params={'count': count, 'offset': offset})
        if response.status_code == 200:
            res = response.json()
            has_more = res['has-more']
            offset = res['offset']
            contacts = res['contacts']
            all_list.extend(contacts)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_list


def main():
    print('you have launched lists.py as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')