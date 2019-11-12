__all__ = ['constants', 'oauth', 'companies', 'contacts', 'associations', 'deals', 'engagements', 'owners']

from .constants import *
from . import oauth, companies, contacts, associations, deals, engagements, owners


def main():
    print('main in hubspot.__init__.py: ok')
    return


parameters = {}

try:
    last = getmtime(AUTHORIZATION_TOKEN_FILE)
    now = datetime.datetime.now().timestamp()
    if (now - last) >= 18000:
        print('The token has expired. I am about to refresh it')
        refre = 'y' # input('y/n? ')
        if refre.startswith('y'):
            res = oauth.refresh_oauth_token()
            if res:
                print('Token refreshed')
            else:
                print('Token not refreshed, something has gone wrong')
except:
    print('No token file')
    pass

token_file = open(AUTHORIZATION_TOKEN_FILE, 'r')
authorization_token = token_file.read()
token_file.close()


if __name__ == '__main__':
    main()
