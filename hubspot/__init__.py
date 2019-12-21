__all__ = ['constants', 'oauth', 'companies', 'contacts',
           'associations', 'deals', 'engagements', 'owners', 'crm_objects']

from . import oauth
import datetime
from os.path import getmtime

try:
    last = getmtime('/home/alxfed/credo/authorization_token.txt')
    now = datetime.datetime.now().timestamp()
    if (now - last) >= 18000:
        print('The token has expired. I am about to refresh it')
        res = oauth.refresh_oauth_token()
        if res:
            print('Token refreshed')
        else:
            print('Token not refreshed, something has gone wrong')
except:
    print('Did not manage to refresh the token')