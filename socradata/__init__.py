__all__ = ['constants', 'meta', 'datasets']

from .constants import *
from . import meta, datasets


def main():
    print('main in socradata.__init__.py: ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')