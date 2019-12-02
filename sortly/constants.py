# -*- coding: utf-8 -*-
"""...
"""
from os import environ

AUTH_TOKEN_FILE             = '/home/alxfed/credo/sortly_auth_token.txt'
REFRESH_TOKEN_FILE          = '/home/alxfed/credo/sortly_secret.txt'

token_file = open(AUTH_TOKEN_FILE, 'r')
authorization_token = token_file.read()
token_file.close()

bearer_string = f'Bearer {authorization_token}'
authorization_header = {'Authorization': bearer_string,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'}

def main():
    print('sortly constants run as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')