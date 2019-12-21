# -*- coding: utf-8 -*-
"""...
"""
from os import environ
# import datetime
# from os.path import getmtime
# from . import oauth

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
#      last = getmtime('/home/alxfed/credo/authorization_token.txt')
#      now = datetime.datetime.now().timestamp()
#      if (now - last) >= 18000:
#          print('The token has expired. I am about to refresh it')
#          res = oauth.refresh_oauth_token()
#          if res:
#              print('Token refreshed')
#          else:
#              print('Token not refreshed, something has gone wrong')
# except:
#     print('No token file')

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
CRM_ASSOCIATIONS_URL = 'https://api.hubapi.com/crm-associations/v1/associations/'
BATCH_ASSOCIATIONS_URL = 'https://api.hubapi.com/crm-associations/v1/associations/create-batch'

ENGAGEMENTS_URL     = 'https://api.hubapi.com/engagements/v1/engagements'
ASSOCIATED_COMPANY_ENGAGEMENGS_URL = 'https://api.hubapi.com/engagements/v1/engagements/associated/COMPANY/'
ALL_ENGAGEMENTS_URL = 'https://api.hubapi.com/engagements/v1/engagements/paged'

DEALS_ALL_URL       = 'https://api.hubapi.com/deals/v1/deal/paged'
DEAL_URL            = 'https://api.hubapi.com/deals/v1/deal'

OWNERS_URL          = 'https://api.hubapi.com/owners/v2/owners'

# deals stages in the Sales Pipeline
STATES_OF_NAMES = { 'Clients (come in )': '904851',
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

NAMES_OF_STATES = { '904851': 'Clients (come in)',
                    '1112239': 'Make quote',
                    'fc1eda4f-23c1-4031-96da-eaadca9ab73e': 'Design / Estimate / Revisions',
                    'qualifiedtobuy': 'Design / Estimates Completed',
                    '77a731b6-782c-4a38-a8b4-0a7b0d319d23': 'Quote, Ready to be Sent',
                    '1175e2fb-5061-491e-81d6-65f0be6ce51e': 'Quote sent out',
                    '2cd78f67-7bfe-4691-824f-24dd4d33aff2': 'Follow up on quote',
                    '7d4554f7-a7b9-4c69-a348-767f1aee7003': 'Send Out To Measure',
                    '30fab7f0-4585-4d31-be27-7704fea2726b': 'To be Checked for Final Approval by Lead Designer',
                    '92eede52-0557-4bfc-87cd-b8137889908c': 'Approved by Lead Designer',
                    '1112240': 'Ready For Contract',
                    'presentationscheduled': 'Client Approved',
                    '1112241': 'Contract Sent Out',
                    'decisionmakerboughtin': 'Contract Signed',
                    '87d11aa5-37df-4db0-b15d-975a172b34c4': 'Deposit Collected',
                    'contractsent': 'In Production',
                    '98866f99-d958-436c-89c5-2ee8d7d6d62d': 'Production Finished',
                    '1112276': 'Ready For Delivery',
                    '32ae2700-1937-4216-9c2c-0119a715ef17': 'Balance Collected',
                    'closedwon': 'Delivery',
                    'a8b2ecbf-f109-4d00-a813-92962430a892': 'Pick Up',
                    'closedlost': 'Closed / Delivered',
                    '825b606f-cda4-4a4c-a201-9bcf331a8aa3': 'Lost / Never Ordered'}

CLIENTS_COME_IN                     = '904851'
MAKE_QUOTE                          = '1112239'
DESIGN_ESTIMATE_REVISIONS           = 'fc1eda4f-23c1-4031-96da-eaadca9ab73e'
DESIGN_ESTIMATE_COMPLETED           = 'qualifiedtobuy'
QOUTE_READY_TO_BE_SENT              = '77a731b6-782c-4a38-a8b4-0a7b0d319d23'
QUOTE_SENT_OUT                      = '1175e2fb-5061-491e-81d6-65f0be6ce51e'
FOLLOW_UP_ON_QUOTE                  = '2cd78f67-7bfe-4691-824f-24dd4d33aff2'
SEND_OUT_TO_MEASURE                 = '7d4554f7-a7b9-4c69-a348-767f1aee7003'
FINAL_APPROVAL_BY_LEAD_DESIGNER     = '30fab7f0-4585-4d31-be27-7704fea2726b'
APPROVED_BY_LEAD_DESIGNER           = '92eede52-0557-4bfc-87cd-b8137889908c'
READY_FOR_CONTRACT                  = '1112240'
CLIENT_APPROVED                     = 'presentationscheduled'
CONTRACT_SENT_OUT                   = '1112241'
CONTRACT_SIGNED                     = 'decisionmakerboughtin'
DEPOSIT_COLLECTED                   = '87d11aa5-37df-4db0-b15d-975a172b34c4'
IN_PRODUCTION                       = 'contractsent'
PRODUCTION_FINISHED                 = '98866f99-d958-436c-89c5-2ee8d7d6d62d'
READY_FOR_DELIVERY                  = '1112276'
BALANCE_COLLECTED                   = '32ae2700-1937-4216-9c2c-0119a715ef17'
DELIVERY                            = 'closedwon'
PICK_UP                             = 'a8b2ecbf-f109-4d00-a813-92962430a892'
CLOSED_DELIVERED                    = 'closedlost'
LOST_NEVER_ORDERED                  = '825b606f-cda4-4a4c-a201-9bcf331a8aa3'

LIST_OF_STATES = ['904851', '1112239', 'fc1eda4f-23c1-4031-96da-eaadca9ab73e', 'qualifiedtobuy',
                  '77a731b6-782c-4a38-a8b4-0a7b0d319d23', '1175e2fb-5061-491e-81d6-65f0be6ce51e',
                  '2cd78f67-7bfe-4691-824f-24dd4d33aff2', '7d4554f7-a7b9-4c69-a348-767f1aee7003',
                  '30fab7f0-4585-4d31-be27-7704fea2726b', '92eede52-0557-4bfc-87cd-b8137889908c',
                  '1112240', 'presentationscheduled', '1112241', 'decisionmakerboughtin',
                  '87d11aa5-37df-4db0-b15d-975a172b34c4', 'contractsent',
                  '98866f99-d958-436c-89c5-2ee8d7d6d62d', '1112276', '32ae2700-1937-4216-9c2c-0119a715ef17',
                  'closedwon', 'a8b2ecbf-f109-4d00-a813-92962430a892', 'closedlost',
                  '825b606f-cda4-4a4c-a201-9bcf331a8aa3']

IDS_OF_OWNERS = {'Alexander Doroshko': '31831742', 'Melissa Conroy': '31831770', 'Douglas Sumner': '33661209',
                 'Bjorn Berkmortel': '34421936', 'Bulat Bakhtiyarov': '35511845', 'Iuliana Midari': '36261319',
                 'Anastasiia Yashchenko': '37489009', 'Dorina Braescu': '38144553'}
                # Daniel is no longer on the list but I know that he owns a contact 1066501, can look his old id there

OWNERS_OF_IDS = {'31831742': 'Alexander Doroshko', '31831770': 'Melissa Conroy', '33661209': 'Douglas Sumner',
                 '34421936': 'Bjorn Berkmortel', '35511845': 'Bulat Bakhtiyarov', '36261319': 'Iuliana Midari',
                 '37489009': 'Anastasiia Yashchenko', '38144553': 'Dorina Braescu'}

OAUTH_TOKEN_URL     = 'https://api.hubapi.com/oauth/v1/token'