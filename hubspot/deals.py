# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants


def create_a_deal(parameters, associations):
    data = {"associations": {},"properties": []}
    data['associations'] = associations
    res = {}
    list_of_properties = []
    for parameter in parameters:
        prop = {"name": parameter,
                "value": parameters[parameter]}
        list_of_properties.append(prop)
    data['properties'] = list_of_properties
    response = requests.request("POST", url=constants.DEAL_URL, json=data,
                                headers=constants.header, params=constants.parameters)
    if response.status_code == 200:
        res = response.json()
        print('deal for permit ', parameters['permit_'], ' created')
    else:
        print('not ok! ', response.status_code)
    return res


def get_all_deal_properties():
    request_url = 'https://api.hubapi.com/properties/v1/deals/properties'
    response = requests.request('GET', url=request_url,
                                headers=constants.authorization_header)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def create_a_deal_oauth(parameters, associations):
    data = {"associations": {},"properties": []}
    data['associations'] = associations
    res = {}
    list_of_properties = []
    for parameter in parameters:
        prop = {"name": parameter,
                "value": parameters[parameter]}
        list_of_properties.append(prop)
    data['properties'] = list_of_properties
    response = requests.request("POST", url=constants.DEAL_URL, json=data,
                                headers=constants.authorization_header)
    if response.status_code == 200:
        res = response.json()
        print('deal for permit ', parameters['permit_'], ' created')
    else:
        print('not ok! ', response.status_code)
    return res


def get_a_deal(dealId):
    request_url = f'{constants.DEAL_URL}/{dealId}'
    response = requests.request('GET', url=request_url,
                                headers=constants.authorization_header,
                                params=constants.parameters)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def update_a_deal(dealId, parameters):
    request_url = f'{constants.DEAL_URL}/{dealId}'
    properties = {"properties": []}
    for key in parameters:
        properties['properties'].append({'name': key, 'value': parameters[key]})
    response = requests.request('PUT', url=request_url,
                                headers=constants.header,
                                json=properties,
                                params=constants.parameters)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def update_a_deal_oauth(dealId, parameters):
    request_url = f'{constants.DEAL_URL}/{dealId}'
    properties = {"properties": []}
    for key, value in parameters.items():
        properties['properties'].append({'name': key, 'value': value})
    response = requests.request('PUT', url=request_url,
                                headers=constants.authorization_header,
                                json=properties)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def batch_update_deals(deals_list:list, parameters:dict):
    all_list = []
    properties = []
    for key, value in parameters.items():
        property = {'name': key, 'value': value}
        properties.append(property)

    each = {'objectId': '', 'properties': properties}
    for deal in deals_list:
        this = each.copy()
        this['objectId'] = deal
        all_list.append(this)

    response = requests.request('POST', url=constants.BATCH_DEALS_UPDATE,
                                headers=constants.authorization_header,
                                json=all_list)
    if response.status_code == 202:
        return
    else:
        print(response.status_code)
    return
'''
[
  {
    "objectId": 93630457,
    "properties": [
      {
        "name": "dealname",
        "value": "Updated deal name."
      }
    ]
  },
  {
    "objectId": 26448234,
    "properties": [
      {
        "name": "dealname",
        "value": "Another updated deal"
      },
      {
        "name": "amount",
        "value": 27
      }
    ]
  }
]
'''

def get_all_deals(request_parameters, include_associations):
    """Downloads the complete list of deals from the portal
    :param request_parameters: list of Deal parameters
    :param include_associations: boolean
    :return all_deals: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    # includeAssociations=true
    def make_parameters_string(include_associations, parameters_substring, offset, limit):
        authentication = 'hapikey=' + constants.api_key
        associations = ''
        if include_associations:
            associations = '&includeAssociations=true'
        parameters_string = f'{authentication}{associations}{parameters_substring}&offset={offset}&limit={limit}'
        return parameters_string
    # prepare for the inevitable output
    all_deals    = []
    output_columns  = ['dealId', 'isDeleted']
    if include_associations:
        assoc_columns = ['associatedVids', 'associatedTicketIds', 'associatedCompanyIds', 'associatedDealIds']
        output_columns.extend(assoc_columns)
    output_columns.extend(request_parameters)

    # package the parameters into a substring
    param_substring = ''
    for item in request_parameters:
        param_substring = '{}&properties={}'.format(param_substring, item)

    # prepare for the pagination
    has_more = True
    offset = 0
    limit = 250  # max 250

    # Now the main cycle
    while has_more:
        api_url = '{}?{}'.format(constants.DEALS_ALL_URL,
                                 make_parameters_string(include_associations,
                                                        param_substring,
                                                        offset, limit)
                                 )
        response = requests.request("GET", url=api_url, headers=constants.header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['hasMore']
            offset      = res['offset']
            deals       = res['deals']
            for deal in deals:
                row = {}
                row.update({"dealId"    : deal["dealId"],
                            "isDeleted" : deal["isDeleted"]
                            })
                if include_associations:
                    de_associations = deal['associations']
                    # 'associatedVids', 'associatedCompanyIds', 'associatedDealIds', 'associatedTicketIds'
                    row.update({'associatedVids'        : ' '.join(map(str, de_associations['associatedVids'])),
                                'associatedCompanyIds'  : ' '.join(map(str, de_associations['associatedCompanyIds'])),
                                'associatedDealIds'     : ' '.join(map(str, de_associations['associatedDealIds'])),
                                'associatedTicketIds'   : ' '.join(map(str, de_associations['associatedTicketIds']))
                                })
                de_properties = deal['properties']
                for de_property in de_properties:
                    if de_property not in output_columns:
                        output_columns.append(de_property)
                        print('Adding a property to colunms list: ', de_property)
                    row.update({de_property: de_properties[de_property]['value']})
                all_deals.append(row)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_deals, output_columns


def get_all_deals_oauth(request_parameters, include_associations):
    """Downloads the complete list of deals from the portal
    :param request_parameters: list of Deal parameters
    :param include_associations: boolean
    :return all_deals: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    # includeAssociations=true
    def make_parameters_string(include_associations, parameters_substring, offset, limit):
        associations = ''
        if include_associations:
            associations = 'includeAssociations=true'
        parameters_string = f'{associations}{parameters_substring}&offset={offset}&limit={limit}'
        return parameters_string
    # prepare for the inevitable output
    all_deals    = []
    output_columns  = ['dealId', 'isDeleted']
    if include_associations:
        assoc_columns = ['associatedVids', 'associatedTicketIds', 'associatedCompanyIds', 'associatedDealIds']
        output_columns.extend(assoc_columns)
    output_columns.extend(request_parameters)

    # package the parameters into a substring
    param_substring = ''
    for item in request_parameters:
        param_substring = '{}&properties={}'.format(param_substring, item)

    # prepare for the pagination
    has_more = True
    offset = 0
    limit = 250  # max 250

    # Now the main cycle
    while has_more:
        api_url = '{}?{}'.format(constants.DEALS_ALL_URL,
                                 make_parameters_string(include_associations,
                                                        param_substring,
                                                        offset, limit)
                                 )
        response = requests.request("GET", url=api_url, headers=constants.authorization_header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['hasMore']
            offset      = res['offset']
            deals       = res['deals']
            for deal in deals:
                row = {}
                row.update({"dealId"    : deal["dealId"],
                            "isDeleted" : deal["isDeleted"]
                            })
                if include_associations:
                    de_associations = deal['associations']
                    # 'associatedVids', 'associatedCompanyIds', 'associatedDealIds', 'associatedTicketIds'
                    row.update({'associatedVids'        : ' '.join(map(str, de_associations['associatedVids'])),
                                'associatedCompanyIds'  : ' '.join(map(str, de_associations['associatedCompanyIds'])),
                                'associatedDealIds'     : ' '.join(map(str, de_associations['associatedDealIds'])),
                                'associatedTicketIds'   : ' '.join(map(str, de_associations['associatedTicketIds']))
                                })
                de_properties = deal['properties']
                for de_property in de_properties:
                    if de_property not in output_columns:
                        output_columns.append(de_property)
                        print('Adding a property to colunms list: ', de_property)
                    row.update({de_property: de_properties[de_property]['value']})
                all_deals.append(row)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_deals, output_columns


def get_first_page_of_deals_oauth(request_parameters, include_associations):
    """Downloads the complete list of deals from the portal
    :param request_parameters: list of Deal parameters
    :param include_associations: boolean
    :return all_deals: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    # includeAssociations=true
    def make_parameters_string(include_associations, parameters_substring, offset, limit):
        associations = ''
        if include_associations:
            associations = 'includeAssociations=true'
        parameters_string = f'{associations}{parameters_substring}&offset={offset}&limit={limit}'
        return parameters_string
    # prepare for the inevitable output
    all_deals    = []
    output_columns  = ['dealId', 'isDeleted']
    if include_associations:
        assoc_columns = ['associatedVids', 'associatedTicketIds', 'associatedCompanyIds', 'associatedDealIds']
        output_columns.extend(assoc_columns)
    output_columns.extend(request_parameters)

    # package the parameters into a substring
    param_substring = ''
    for item in request_parameters:
        param_substring = '{}&properties={}'.format(param_substring, item)

    # prepare for the pagination
    has_more = True
    offset = 0
    limit = 250  # max 250

    # Now the main cycle
    api_url = '{}?{}'.format(constants.DEALS_ALL_URL,
                             make_parameters_string(include_associations,
                                                    param_substring,
                                                    offset, limit)
                             )
    response = requests.request("GET", url=api_url, headers=constants.authorization_header)
    if response.status_code == 200:
        res = response.json()
        deals = res['deals']
        for deal in deals:
            row = {}
            row.update({"dealId"    : deal["dealId"],
                        "isDeleted" : deal["isDeleted"]
                        })
            if include_associations:
                de_associations = deal['associations']
                # 'associatedVids', 'associatedCompanyIds', 'associatedDealIds', 'associatedTicketIds'
                row.update({'associatedVids'        : ' '.join(map(str, de_associations['associatedVids'])),
                            'associatedCompanyIds'  : ' '.join(map(str, de_associations['associatedCompanyIds'])),
                            'associatedDealIds'     : ' '.join(map(str, de_associations['associatedDealIds'])),
                            'associatedTicketIds'   : ' '.join(map(str, de_associations['associatedTicketIds']))
                            })
            de_properties = deal['properties']
            for de_property in de_properties:
                if de_property not in output_columns:
                    output_columns.append(de_property)
                    print('Adding a property to colunms list: ', de_property)
                row.update({de_property: de_properties[de_property]['value']})
            all_deals.append(row)
        print('Now at offset: ', offset)
    else:
        print(response.status_code)
    return all_deals, output_columns


def main():
    print('You have launched this module as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')