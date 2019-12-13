# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants


def create_company(parameters):
    """
    :param parameters:  dictionary of company properties
    :return: json
    """
    res = {}
    data = {"properties": []}
    list_of_properties = []
    for parameter in parameters:
        prop = {"name" : parameter,
                "value": parameters[parameter]}
        list_of_properties.append(prop)
    data['properties'] = list_of_properties
    response = requests.request("POST", url=constants.COMPANY_CREATE_URL, json=data,
                                headers=constants.authorization_header, params=constants.parameters)
    if response.status_code == 200:
        res = response.json()
    else:
        print('not ok! ', response.status_code)
    return res


def update_company(companyId, parameters):
    request_url = f'{constants.COMPANY_UPDATE_URL}{companyId}'
    response = requests.request('PUT', url=request_url,
                                headers=constants.header,
                                json=parameters,
                                params=constants.parameters)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def search_for_company_by_domain(domain, paramlist):
    payload = {
              "limit": 2,
              "requestOptions": {
                "properties": paramlist
                },
              "offset": {
                "isPrimary": True,
                "companyId": 0
                }
              }
    request_url = f'{constants.COMPANY_SEARCH_URL}{domain}/companies'
    response = requests.request('POST', url=request_url,
                                headers=constants.header,
                                json=payload,
                                params=constants.parameters)
    if response.status_code == 200:
        resp = response.json()
        return resp
    else:
        print(response.status_code)
        return


def get_all_companies_key(request_parameters):
    """Downloads the complete list of companies from the portal
    :param request_parameters: list of Contact parameters
    :return all_companies: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    def make_parameters_string(parameters_substring, offset, limit):
        authentication = 'hapikey=' + constants.api_key
        parameters_string = f'{authentication}{parameters_substring} \
                                &offset={offset}&limit={limit}'
        return parameters_string
    # prepare for the (inevitable) output
    all_companies    = []
    output_columns  = ['companyId', 'isDeleted']
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
        api_url = '{}?{}'.format(constants.COMPANIES_ALL_URL,
                                 make_parameters_string(param_substring, offset, limit))
        response = requests.request("GET", url=api_url, headers=constants.header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['has-more']
            offset      = res['offset']
            companies   = res['companies']
            for company in companies:
                row = {}
                row.update({"companyId": company["companyId"],
                            "isDeleted": company["isDeleted"]})
                co_properties = company['properties']
                for co_property in co_properties:
                    if co_property not in output_columns:
                        output_columns.append(co_property)
                        print('Adding a property to colunms list: ', co_property)
                    row.update({co_property: co_properties[co_property]['value']})
                all_companies.append(row)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_companies, output_columns


def get_all_companies_oauth(request_parameters):
    """Downloads the complete list of companies from the portal
    :param request_parameters: list of Contact parameters
    :return all_companies: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    def make_parameters_string(parameters_substring, offset, limit):
        # authentication = 'hapikey=' + constants.api_key
        parameters_string = f'{parameters_substring}&offset={offset}&limit={limit}'
        return parameters_string
    # prepare for the (inevitable) output
    all_companies    = []
    output_columns  = ['companyId', 'isDeleted']
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
        api_url = '{}?{}'.format(constants.COMPANIES_ALL_URL,
                                 make_parameters_string(param_substring, offset, limit))
        response = requests.request("GET", url=api_url, headers=constants.authorization_header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['has-more']
            offset      = res['offset']
            companies   = res['companies']
            for company in companies:
                row = {}
                row.update({"companyId": company["companyId"],
                            "isDeleted": company["isDeleted"]})
                co_properties = company['properties']
                for co_property in co_properties:
                    if co_property not in output_columns:
                        output_columns.append(co_property)
                        print('Adding a property to columns list: ', co_property)
                    row.update({co_property: co_properties[co_property]['value']})
                all_companies.append(row)
            print('Now at offset: ', offset)
        else:
            print(response.status_code)
    return all_companies, output_columns


def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')