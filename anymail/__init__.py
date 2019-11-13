__all__ = ['constants', 'find', 'verify']

from .constants import *
from . import find, verify


def main():
    print('You have launched anymail __init__.py as main')
    return


key_file = open(AUTHORIZATION_KEY_FILE, 'r')
anymail_api_key = key_file.read()
key_file.close()

# use this header with all the API calls
headers = {'X-Api-Key': anymail_api_key}


if __name__ == '__main__':
    main()
    print('main - done')