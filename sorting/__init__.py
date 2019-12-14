__all__ = ['constants', 'companies', 'inspections']

from .constants import *
from . import companies, inspections


def main():
    print('main in socradata.__init__.py: ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')