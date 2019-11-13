# -*- coding: utf-8 -*-
"""...
"""


credits_check_url = 'https://api.anymailfinder.com/v4.1/account/hits_left.json'
api_url = 'https://api.anymailfinder.com/v4.1/search/company.json'

AUTHORIZATION_KEY_FILE = '/home/alxfed/credo/anymail_key.txt'

key_file = open(AUTHORIZATION_KEY_FILE, 'r')
anymail_api_key = key_file.read()
key_file.close()

# use this header with all the API calls
headers = {'X-Api-Key': anymail_api_key}


def main():
    print('You launched the constants.py as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')