# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants


def parse_engagement_response(one_result):
    data = {}
    engagement      = one_result['engagement']
    associations    = one_result['associations']
    attachments     = one_result['attachments']
    metadata        = one_result['metadata']
    # engagement
    for key in engagement:
        data.update({key: engagement[key]})
    # associations
    for key in associations:
        data.update({key: ' '.join(map(str, associations[key]))})
    # attachments
    data.update({'attachments': ' '.join(map(str, attachments))})
    # metadata
    data.update({'metadata': metadata})
    return data


def package_engagement_data(data):
    engagement = {"engagement": {
        "active": 'true',
        "ownerId": data['ownerId'],
        "type": "NOTE",
        "timestamp": data['timestamp']
    },
        "associations": {
            "contactIds": [],
            "companyIds": [],
            "dealIds": [data['dealId']],
            "ownerIds": [data['ownerId']]
        },
        "attachments": [
            {
                "id": ''
            }
        ],
        "metadata": {
            "body": data['note']
        }
    }
    return engagement


def create_engagement_note(parameters):
    created_note = {}
    companyId = ''
    dealIds = ''
    if 'companyId' in parameters.keys(): companyId = str(parameters['companyId'])
    if 'dealIds' in parameters.keys(): dealIds = str(parameters['dealIds'])
    data = {"engagement": {
                    "active": 'true',
                    "ownerId": str(parameters['ownerId']),
                    "type": "NOTE",
                    "timestamp": str(parameters['timestamp'])
                },
                "associations": {
                    "contactIds": [],
                    "companyIds": [companyId],
                    "dealIds": dealIds,
                    "ownerIds": [str(parameters['ownerId'])]
                },
                "attachments": [
                    {
                        "id": ''
                    }
                ],
                "metadata": {
                    "body": parameters['note']
                }
            }

    response = requests.request(method="POST", url=constants.ENGAGEMENTS_URL,
                                json=data, headers=constants.authorization_header)
    if response.status_code == 200:
        created_note = response.json()
        print('Created a note to company ', companyId)
    else:
        print('not ok! ', response.status_code)
    return created_note


def get_an_engagement(engagementId):
    data = {}
    api_uri = constants.ENGAGEMENTS_URL + f'/{engagementId}'
    response = requests.request("GET", url=api_uri, headers=constants.authorization_header)
    if response.status_code == 200:
        data = parse_engagement_response(response.json())
    else:
        print('Not ok: ', response.status_code)
    return data


def update_an_engagement(engagementId, parameters):
    # /engagements/v1/engagements/engagementId
    updated_note = {}
    data = {}
    if 'timestamp' in parameters.keys():
        data.update({"engagement": {"timestamp": parameters['timestamp']}})
    if 'dealIds' in parameters.keys():
        data.update({"associations": {"dealIds": parameters['dealIds']}})
    if 'note' in parameters.keys():
        data.update({"metadata": {"body": parameters['note']}})
    # data = {"engagement": {"timestamp": parameters['timestamp']},
    #         "associations": {"dealIds": parameters['dealIds']},
    #         "metadata": {"body": parameters['note']}
    #         }
    #
    URL = constants.ENGAGEMENTS_URL + f'/{engagementId}'
    response = requests.request("PATCH", url=URL, json=data,
                                headers=constants.authorization_header)
    if response.status_code == 200:
        updated_note = response.json()
        print('Updated an engagement Note ')
    else:
        print('not ok! The note has not been updated', response.status_code)
    return updated_note


def delete_an_engagement(engagementId):
    outcome = False
    api_uri = constants.ENGAGEMENTS_URL + f'/{engagementId}'
    response = requests.request("DELETE", url=api_uri, headers=constants.authorization_header)
    if response.status_code == 204:
        outcome = True
    return outcome


def get_all_engagements_oauth():
    """Downloads the complete list of engagements from the portal
    :return all_engagements: list of dictionaries
    :return all_columns: list of all columns
    """
    all_columns = ["id", "portalId", "active", "createdAt", "lastUpdated",
                   "type", "timestamp",
                   'contactIds', 'companyIds', 'dealIds', 'ownerIds', 'workflowIds',
                   'ticketIds', 'contentIds', 'quoteIds',
                   'attachments', 'metadata']
    all_engagements = []
    # prepare for the pagination
    has_more = True
    offset = 0
    limit = 250  # max 250

    # Now the main cycle
    while has_more:
        api_url = constants.ALL_ENGAGEMENTS_URL + f'?offset={offset}&limit={limit}'
        response = requests.request("GET", url=api_url, headers=constants.authorization_header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['hasMore']
            offset      = res['offset']
            results     = res['results']
            for result in results:
                engagement      = result['engagement']
                associations    = result['associations']
                attachments     = result['attachments']
                metadata        = result['metadata']
                row = {}
                row.update({"id"            : engagement["id"],
                            "portalId"      : engagement["portalId"],
                            "active"        : engagement["active"],
                            "createdAt"     : engagement["createdAt"],
                            "lastUpdated"   : engagement["lastUpdated"],
                            "type"          : engagement["type"],
                            "timestamp"     : engagement["timestamp"]
                            })
                # associations
                row.update({'contactIds'    : ' '.join(map(str, associations['contactIds'])),
                            'companyIds'    : ' '.join(map(str, associations['companyIds'])),
                            'dealIds'       : ' '.join(map(str, associations['dealIds'])),
                            'ownerIds'      : ' '.join(map(str, associations['ownerIds'])),
                            'workflowIds'   : ' '.join(map(str, associations['workflowIds'])),
                            'ticketIds': ' '.join(map(str, associations['ticketIds'])),
                            'contentIds': ' '.join(map(str, associations['contentIds'])),
                            'quoteIds': ' '.join(map(str, associations['quoteIds']))
                            })
                # attachments
                row.update({'attachments': ' '.join(map(str, attachments))})
                # metadata
                row.update({'metadata': metadata})
                all_engagements.append(row)
            # has_more = False
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_engagements, all_columns


def get_engagements_of_object(companyId:str) -> list:
    list_of_engagements = []
    URL = constants.ASSOCIATED_COMPANY_ENGAGEMENGS_URL + f'{companyId}' + '/paged'
    parameters = {'offset': '', 'limit': ''}
    offset = 0
    limit = 100  # max 100
    has_more = True

    # Now the main cycle
    while has_more:
        parameters['offset'] = offset
        parameters['limit'] = limit
        response = requests.request("GET", url=URL,
                                    headers=constants.authorization_header,
                                    params=parameters)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['hasMore']
            offset      = res['offset']
            results     = res['results']
            for result in results:
                engagement      = result['engagement']
                associations    = result['associations']
                attachments     = result['attachments']
                metadata        = result['metadata']
                row = {}
                row.update({"id"            : engagement["id"],
                            "portalId"      : engagement["portalId"],
                            "active"        : engagement["active"],
                            "createdAt"     : engagement["createdAt"],
                            "lastUpdated"   : engagement["lastUpdated"],
                            "type"          : engagement["type"],
                            "timestamp"     : engagement["timestamp"]
                            })
                # associations
                row.update({'contactIds'    : ' '.join(map(str, associations['contactIds'])),
                            'companyIds'    : ' '.join(map(str, associations['companyIds'])),
                            'dealIds'       : ' '.join(map(str, associations['dealIds'])),
                            'ownerIds'      : ' '.join(map(str, associations['ownerIds'])),
                            'workflowIds'   : ' '.join(map(str, associations['workflowIds'])),
                            'ticketIds'     : ' '.join(map(str, associations['ticketIds'])),
                            'contentIds'    : ' '.join(map(str, associations['contentIds'])),
                            'quoteIds'      : ' '.join(map(str, associations['quoteIds']))
                            })
                # attachments
                row.update({'attachments': ' '.join(map(str, attachments))})
                # metadata
                row.update({'metadata': metadata})
                list_of_engagements.append(row)
            # has_more = False
            print('Now at offset: ', offset)
        else:
            print(response.status_code)

    return list_of_engagements


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')