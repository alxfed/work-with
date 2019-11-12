# -*- coding: utf-8 -*-
"""...
"""
import requests
from hubspot import constants
from os import environ


# Get OAuth 2.0 Access Token and Refresh Tokens
def get_oauth_token():
    '''
    https://developers.google.com/oauthplayground/#step1&url=https%3A%2F%2F&content_type=application%2Fjson&http_method=GET&useDefaultOauthCred=unchecked&oauthEndpointSelect=Custom&oauthAuthEndpointValue=https%3A%2F%2Fapp.hubspot.com%2Foauth%2Fauthorize&oauthTokenEndpointValue=https%3A%2F%2Fapi.hubapi.com%2Foauth%2Fv1%2Ftoken&includeCredentials=checked&accessTokenType=bearer&autoRefreshToken=unchecked&accessType=offline&prompt=consent&response_type=code
    :return:
    '''
    authorization_token = ''
    headers = constants.oauth_header
    client_id = environ['client_id']
    client_secret = environ['client_secret']
    redir = environ['redirect_uri']  # redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground
    code = environ['code']
    data = f'grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redir}&code={code}'
    res = requests.request('POST', url=constants.OAUTH_TOKEN_URL, data=data, headers=headers)
    if res.status_code == 400:
        print('400')
        return
    else:
        response = res.json()
        refresh_token_file = './refresh_token.txt'
        authorization_token_file = './authorization_token.txt'
        rtf = open(refresh_token_file, 'w')
        refresh_token = response['refresh_token']
        rtf.write(refresh_token)
        rtf.close()
        atf = open(authorization_token_file, 'w')
        authorization_token = response['access_token']
        atf.write(authorization_token)
        atf.close()
    return authorization_token


def refresh_oauth_token():
    rtf = open(constants.REFRESH_TOKEN_FILE, 'r')
    refresh_token = rtf.read()
    rtf.close()
    headers = constants.oauth_header
    clid = open(constants.CLIENT_ID_FILE, 'r')
    client_id = clid.read()
    clid.close()
    clsc = open(constants.CLIENT_SECRET_FILE, 'r')
    client_secret = clsc.read()
    clsc.close()
    data = f'grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
    response = requests.request('POST', url=constants.OAUTH_TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        res = response.json()
        refresh_token = res['refresh_token']
        rtf = open(constants.REFRESH_TOKEN_FILE, 'w')
        rtf.write(refresh_token)
        rtf.close()
        authorization_token = res['access_token']
        autf = open(constants.AUTHORIZATION_TOKEN_FILE, 'w')
        autf.write(authorization_token)
        autf.close()
        return True
    elif response.status_code == 400:
        return False
    else:
        print('Not 200 but not 400 either')
        return


def main():
    res = refresh_oauth_token()
    return


if __name__ == '__main__':
    main()
    print('main - done')