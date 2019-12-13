# -*- coding: utf-8 -*-
"""...
"""
from os import environ
import datetime
from os.path import getmtime
from . import oauth

# credentials files
AUTHORIZATION_TOKEN_FILE    = '/home/alxfed/credo/authorization_token.txt'
REFRESH_TOKEN_FILE          = '/home/alxfed/credo/refresh_token.txt'
CLIENT_ID_FILE              = '/home/alxfed/credo/client_id.txt'
CLIENT_SECRET_FILE          = '/home/alxfed/credo/client_secret.txt'

parameters = {}
if 'API_KEY' in environ.keys():
    api_key = environ['API_KEY']
    parameters = {'hapikey': api_key}

# try:
#     last = getmtime(AUTHORIZATION_TOKEN_FILE)
#     now = datetime.datetime.now().timestamp()
#     if (now - last) >= 18000:
#         print('The token has expired. I am about to refresh it')
#         refre = 'y' # input('y/n? ')
#         if refre.startswith('y'):
#             res = oauth.refresh_oauth_token()
#             if res:
#                 print('Token refreshed')
#             else:
#                 print('Token not refreshed, something has gone wrong')
# except:
#     print('No token file')
#     pass

token_file = open(AUTHORIZATION_TOKEN_FILE, 'r')
authorization_token = token_file.read()
token_file.close()

bearer_string = f'Bearer {authorization_token}'
authorization_header = {'Authorization': bearer_string, 'Content-Type': 'application/json'}
header = {'Content-Type': 'application/json'}
oauth_header = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

COMPANY_CREATE_URL  = 'https://api.hubapi.com/companies/v2/companies'
COMPANY_DELETE_URL  = 'https://api.hubapi.com/companies/v2/companies/'
COMPANY_UPDATE_URL  = 'https://api.hubapi.com/companies/v2/companies/'
COMPANY_SEARCH_URL  = 'https://api.hubapi.com/companies/v2/domains/'
COMPANIES_ALL_URL   = 'https://api.hubapi.com/companies/v2/companies/paged'

CONTACT_URL         = 'https://api.hubapi.com/contacts/v1/contact'
LISTS_ALL_URL       = 'https://api.hubapi.com/contacts/v1/lists'
CONTACTS_ALL_URL    = 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all'
CONTACT_SEARCH_QUERY_URL = 'https://api.hubapi.com/contacts/v1/search/query?q='

ASSOCIATIONS_URL    = 'https://api.hubapi.com/crm-associations/v1/associations'

ENGAGEMENTS_URL     = 'https://api.hubapi.com/engagements/v1/engagements'
ALL_ENGAGEMENTS_URL = 'https://api.hubapi.com/engagements/v1/engagements/paged'

DEALS_ALL_URL       = 'https://api.hubapi.com/deals/v1/deal/paged'
DEAL_URL            = 'https://api.hubapi.com/deals/v1/deal'

OWNERS_URL          = 'https://api.hubapi.com/owners/v2/owners'

# deals stages in the Sales Pipeline
sales_stages = {'Clients (come in )': '904851',
                'Received layout': 'bd8039e1-8b13-4840-a5cb-95c9aff3067c',
                'Make quote': '1112239',
                'Design / Estimate / Revisions': 'fc1eda4f-23c1-4031-96da-eaadca9ab73e',
                'Design / Estimates Completed': 'qualifiedtobuy',
                'Quote, Ready to be Sent': '77a731b6-782c-4a38-a8b4-0a7b0d319d23',
                'Quote sent out': '1175e2fb-5061-491e-81d6-65f0be6ce51e',
                'Follow up on quote': '2cd78f67-7bfe-4691-824f-24dd4d33aff2',
                'Send Out To Measure': '7d4554f7-a7b9-4c69-a348-767f1aee7003',
                'To be Checked for Final Approval by Lead Designer': '30fab7f0-4585-4d31-be27-7704fea2726b',
                'Approved by Lead Designer': '92eede52-0557-4bfc-87cd-b8137889908c',
                'Ready For Contract': '1112240',
                'Client Approved': 'presentationscheduled',
                'Contract Sent Out': '1112241',
                'Contract Signed': 'decisionmakerboughtin',
                'Deposit Collected': '87d11aa5-37df-4db0-b15d-975a172b34c4',
                'In Production': 'contractsent',
                'Production Finished': '98866f99-d958-436c-89c5-2ee8d7d6d62d',
                'Ready For Delivery': '1112276',
                'Balance Collected': '32ae2700-1937-4216-9c2c-0119a715ef17',
                'Delivery': 'closedwon',
                'Pick Up': 'a8b2ecbf-f109-4d00-a813-92962430a892',
                'Closed / Delivered': 'closedlost',
                'Lost / Never Ordered': '825b606f-cda4-4a4c-a201-9bcf331a8aa3'}

OAUTH_TOKEN_URL     = 'https://api.hubapi.com/oauth/v1/token'