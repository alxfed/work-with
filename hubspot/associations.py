# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants


def get_associations_of_object(object_id, association_type):
    """Get a list of associated objects for an object
    for a given type of association
    :param object_id:
    :param association_type:
    :return: list of ids of associated objects
    """
    list_of_associated_objects = []
    offset = 0
    limit = 100
    has_more = True

    while has_more:
        authentication = 'hapikey=' + constants.api_key
        api_url = f'{constants.ASSOCIATIONS_URL}/{object_id}/HUBSPOT_DEFINED/' \
                  f'{str(association_type)}?{authentication}&offset={offset}&limit={limit}'
        response = requests.request("GET", url=api_url, headers=constants.header)
        if response.status_code == 200:
            res = response.json()
            has_more = res['hasMore']
            offset = res['offset']
            list_of_associated_objects.extend(res['results'])
        else:
            print('Error: ', response.status_code)
    return list_of_associated_objects


def get_associations_oauth(object_id, association_type):
    """Get a list of associated objects for an object
    for a given type of association
    :param object_id:
    :param association_type:
    :return: list of ids of associated objects
    """
    list_of_associated_objects = []
    parameters = {'offset': '', 'limit': ''}
    offset = 0
    limit = 100
    has_more = True

    while has_more:
        api_url = f'{constants.ASSOCIATIONS_URL}/{object_id}/HUBSPOT_DEFINED/' \
                  f'{str(association_type)}'
        parameters['offset'] = offset
        parameters['limit'] = limit
        response = requests.request("GET", url=api_url, headers=constants.authorization_header,
                                    params=parameters)
        if response.status_code == 200:
            res = response.json()
            has_more = res['hasMore']
            offset = res['offset']
            list_of_associated_objects.extend(res['results'])
        else:
            print('Error: ', response.status_code)
    return list_of_associated_objects



def create_association_of_objects(from_object_id, to_object_id, association_type):
    """Create an association from one object to another
    :param from_object_id:
    :param to_object_id:
    :param association_type:
    :return:
    """
    connected = False
    data = {
            "fromObjectId": from_object_id,
            "toObjectId": to_object_id,
            "category": "HUBSPOT_DEFINED",
            "definitionId": association_type
            }

    response = requests.request("PUT", url=constants.ASSOCIATIONS_URL,
                                json=data, headers=constants.authorization_header)
    if not response.status_code == 204:
        print('Error: ', response.status_code)
        connected = False
    else:
        connected = True
    return connected


def create_one_to_many_associations(associations_from: str,
                                    association_to: list,
                                    association_type: str) -> bool:
    # prepare json
    associations_to_create = []
    for to in association_to:
        assoc = {
                    "fromObjectId": associations_from,
                    "toObjectId": to,
                    "category": "HUBSPOT_DEFINED",
                    "definitionId": association_type
                }
        associations_to_create.append(assoc)
    created = False
    response = requests.request(
        method="PUT", url=constants.BATCH_ASSOCIATIONS_URL,
        json=associations_to_create, headers=constants.authorization_header)
    if response.status_code == 204:
        created = True
    return created


def main():
    print('You have launched the module as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')