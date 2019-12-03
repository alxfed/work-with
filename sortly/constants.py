# -*- coding: utf-8 -*-
"""...
"""
import sortly

AUTH_TOKEN_FILE             = '/home/alxfed/credo/sortly_secret.txt'
REFRESH_TOKEN_FILE          = '/home/alxfed/credo/sortly_public.txt'

token_file = open(AUTH_TOKEN_FILE, 'r')
authorization_token = token_file.read()
token_file.close()

bearer_string = f'Bearer {authorization_token}'
authorization_header = {'Authorization': bearer_string,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'}

ITEMS_URL               = 'https://api.sortly.co/api/v1/items'
LIST_CUSTOM_FIELDS_URL  = 'https://api.sortly.co/api/v1/custom_fields'

# Sortly-Rate-Limit-Max:1000
sortly_rate_limit_max = 1000
# Sortly-Rate-Limit-Remaining:10
sortly_rate_limit_remaining = 1000
# Sortly-Rate-Limit-Reset:2000
sortly_rate_limit_reset = 2000

def main():
    print('sortly constants run as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')