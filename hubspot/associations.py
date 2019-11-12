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


def create_association_of_objects(from_object_id, to_object_id, association_type):
    """Create an association from one object to another
    :param from_object_id:
    :param to_object_id:
    :param association_type:
    :return:
    """
    data = {
            "fromObjectId": from_object_id,
            "toObjectId": to_object_id,
            "category": "HUBSPOT_DEFINED",
            "definitionId": association_type
            }

    authentication = 'hapikey=' + constants.api_key
    api_url = f'{constants.ASSOCIATIONS_URL}?{authentication}'
    response = requests.request("PUT", url=api_url, json=data, headers=constants.header)
    if not response.status_code == 204:
        print('Error: ', response.status_code)
    return


def main():
    print('You have launched the module as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')