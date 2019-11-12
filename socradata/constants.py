# -*- coding: utf-8 -*-
"""...
"""
import requests as rq

# meta for discovery
# discovery by id: GET http://api.us.socrata.com/api/catalog/v1?ids=ydr8-5enu
# discovery by domain: GET http://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&search_context=data.cityofchicago.org
DISCOVERY_API_URL = 'http://api.us.socrata.com/api/catalog/v1'
CHICAGO_RESOURCE_URL = 'data.cityofchicago.org'

# socrata key authorization
SOCRATA_API_TOKEN_FILE    = '/home/alxfed/credo/socrata_api_token.txt'
token_file = open(SOCRATA_API_TOKEN_FILE, 'r')
socrata_api_token = token_file.read()
token_file.close()

socrata_authorization_header = {'Content-Type': 'application/json', 'X-App-Token': socrata_api_token}

def main():
    return


if __name__ == '__main__':
    main()
    print('main - done')