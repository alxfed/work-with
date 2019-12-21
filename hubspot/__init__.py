import datetime
from os.path import getmtime
from requests import request

AUTHORIZATION_TOKEN_FILE    = '/home/alxfed/credo/authorization_token.txt'
REFRESH_TOKEN_FILE          = '/home/alxfed/credo/refresh_token.txt'
CLIENT_ID_FILE              = '/home/alxfed/credo/client_id.txt'
CLIENT_SECRET_FILE          = '/home/alxfed/credo/client_secret.txt'

oauth_header = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
OAUTH_TOKEN_URL     = 'https://api.hubapi.com/oauth/v1/token'


def refresh_oauth_token():
    rtf = open(REFRESH_TOKEN_FILE, 'r')
    refresh_token = rtf.read()
    rtf.close()
    headers = oauth_header
    clid = open(CLIENT_ID_FILE, 'r')
    client_id = clid.read()
    clid.close()
    clsc = open(CLIENT_SECRET_FILE, 'r')
    client_secret = clsc.read()
    clsc.close()
    data = f'grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
    response = request('POST', url=OAUTH_TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        res = response.json()
        refresh_token = res['refresh_token']
        rtf = open(REFRESH_TOKEN_FILE, 'w')
        rtf.write(refresh_token)
        rtf.close()
        authorization_token = res['access_token']
        autf = open(AUTHORIZATION_TOKEN_FILE, 'w')
        autf.write(authorization_token)
        autf.close()
        return True
    elif response.status_code == 400:
        return False
    else:
        print('Not 200 but not 400 either')
        return


try:
    last = getmtime('/home/alxfed/credo/authorization_token.txt')
    now = datetime.datetime.now().timestamp()
    if (now - last) >= 18000:
        print('Oauth token has expired. I am about to refresh it')
        res = refresh_oauth_token()
        if res:
            print('Token refreshed')
        else:
            print('Token not refreshed, something has gone wrong')
except:
    print('Did not manage to refresh the token')


# now the imports
__all__ = ['constants', 'oauth', 'companies', 'contacts',
           'associations', 'deals', 'engagements', 'owners', 'crm_objects']
from . import constants, oauth, owners, lists, engagements, deals, contacts, constants, companies, associations, crm_objects