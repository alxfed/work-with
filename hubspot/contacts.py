# -*- coding: utf-8 -*-
"""...
"""
import requests
from . import constants
from time import sleep


def search_for_contacts(query_term):
    query = constants.CONTACT_SEARCH_QUERY_URL + query_term
    response = requests.get(url=query, params=constants.parameters)
    if response.status_code == 200:
        re = response.json()
    elif response.status_code > 200:
        print('The query: ', query_term, ' didnt work')
        re = None
    else:
        print('The query: ', query_term, ' returned something weird')
        re = None
    return re


def create_or_update_contact(email:str, properties:dict):
    data = {'properties': [{"property": "firstname","value": ""},
                           {"property": "lastname","value": ""},
                           {"property": "company","value": ""},
                           {"property": "company_index","value": ""},
                           {"property": "jobtitle","value": "Kitchen & Bath Designer employee"}
                           ]}

    data = properties
    response = requests.request(method="POST",
                                url=constants.CONTACT_CREATE_OR_UPDATE_URL,
                                json=data,
                                headers=constants.authorization_header)
    if response.status_code == 200:
        res = response.json()
        has_more = res['has-more']
        vidOffset = res['vid-offset']
        contacts = res['contacts']
        for contact in contacts:
            row = {}
            row.update({"vid": contact["vid"],
                        "is_contact": contact["is-contact"]})
            co_properties = contact['properties']
            for co_property in co_properties:
                if co_property not in output_columns:
                    output_columns.append(co_property)
                    print('Adding a property to colunms list: ', co_property)
                row.update({co_property: co_properties[co_property]['value']})
            all_contacts.append(row)
        print('Now at vidOffset: ', vidOffset)
    else:
        print(response.status_code)

    return


def get_all_contacts(request_parameters):
    """Downloads the complete list of contacts from the portal
    :param request_parameters: list of Contact parameters
    :return all_contacts: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    def make_parameters_string(vidOffset, count):
        authentication = 'hapikey=' + constants.api_key
        parameters_string = '{}{}&vidOffset={}&count={}'.format(authentication,
                                                                param_substring,
                                                                vidOffset, count)
        return parameters_string
    # prepare for the (inevitable) output
    all_contacts    = []
    output_columns  = ['vid', 'is_contact']
    output_columns.extend(request_parameters)

    # package the parameters into a substring
    param_substring = ''
    for item in request_parameters:
        param_substring = '{}&property={}'.format(param_substring, item)

    # prepare for the pagination
    has_more = True
    vidOffset = 0
    count = 100  # max 100

    # Now the main cycle
    while has_more:
        api_url = '{}?{}'.format(constants.CONTACTS_ALL_URL,
                                 make_parameters_string(vidOffset, count))
        response = requests.request("GET", url=api_url, headers=constants.header)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['has-more']
            vidOffset   = res['vid-offset']
            contacts    = res['contacts']
            for contact in contacts:
                row = {}
                row.update({"vid": contact["vid"],
                            "is_contact": contact["is-contact"]})
                co_properties = contact['properties']
                for co_property in co_properties:
                    if co_property not in output_columns:
                        output_columns.append(co_property)
                        print('Adding a property to colunms list: ', co_property)
                    row.update({co_property: co_properties[co_property]['value']})
                all_contacts.append(row)
            print('Now at vidOffset: ', vidOffset)
        else:
            print(response.status_code)
    return all_contacts, output_columns


def get_all_contacts_oauth(request_parameters):
    """Downloads the complete list of contacts from the portal
    :param request_parameters: list of Contact parameters
    :return all_contacts: list of dictionaries / CDR
    :return output_columns: list of output column names
    """
    def make_parameters_string(vidOffset, count):
        parameters_string = '{}&vidOffset={}&count={}'.format(param_substring, vidOffset, count)
        return parameters_string

    # prepare for the (inevitable) output
    all_contacts    = []
    output_columns  = ['vid', 'is_contact']
    output_columns.extend(request_parameters)

    # package the parameters into a substring
    param_substring = ''
    for item in request_parameters:
        param_substring = '{}&property={}'.format(param_substring, item)

    # prepare for the pagination
    has_more = True
    vidOffset = 0
    count = 100  # max 100

    # Now the main cycle
    while has_more:
        api_url = '{}?{}'.format(constants.CONTACTS_ALL_URL,
                                 make_parameters_string(vidOffset, count))
        response = requests.request(method="GET", url=api_url,
                                    headers=constants.authorization_header)
        sleep(.5)
        if response.status_code == 200:
            res = response.json()
            has_more    = res['has-more']
            vidOffset   = res['vid-offset']
            contacts    = res['contacts']
            for contact in contacts:
                row = {}
                row.update({"vid": contact["vid"],
                            "is_contact": contact["is-contact"]})
                co_properties = contact['properties']
                # for co_property in co_properties:
                #     if co_property not in output_columns:
                #         output_columns.append(co_property)
                #         print('Adding a property to colunms list: ', co_property)
                #     row.update({co_property: co_properties[co_property]['value']})
                all_contacts.append(row)
            print('Now at vidOffset: ', vidOffset)
        else:
            print(response.status_code)
    return all_contacts, output_columns


def get_all_contact_properties():
    response = requests.request(method="GET",
                                url=constants.CONTACT_GET_ALL_PROPERTIES,
                                headers=constants.authorization_header)
    if response.status_code == 200:
        properties = response.json()
    else:
        properties = []
        print('Error: ', response.status_code)
    return properties


def get_contact_properties(vid, req_properties):
    """
    get the profile of a contact
    :param vid:
    :return: profile
    """
    # package the parameters into a substring
    properties = {}
    param_substring = ''
    for item in req_properties:
        param_substring = '{}&property={}'.format(param_substring, item)
    authentication = 'hapikey=' + constants.api_key
    api_url = f'{constants.CONTACT_URL}/vid/{vid}/profile?{authentication}{param_substring}'
    response = requests.request("GET", url=api_url, headers=constants.header)
    if response.status_code == 200:
        res = response.json()
        properties= res['properties']
    else:
        print('Error: ', response.status_code)
    return properties


def main():
    print("\nYou've launched the module as __main__\n")
    return


if __name__ == '__main__':
    main()
    print('main - done')