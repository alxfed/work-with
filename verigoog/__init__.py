__all__ = ['constants', 'places']

from .constants import *
from . import places
import googlemaps


def main():
    print('main in verigoog.__init__.py: ok')
    return


token_file = open(ELGOOG_TOKEN_FILE, 'r')
authorization_token = token_file.read()
token_file.close()

Client = googlemaps.Client(key=authorization_token, timeout=10,
                                retry_timeout=2,
                                queries_per_second=1,
                                retry_over_query_limit=True)


if __name__ == '__main__':
    main()
