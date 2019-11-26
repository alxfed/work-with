# -*- coding: utf-8 -*-
"""...
"""
import hubspot


def main():
    name = 'Customers with wrong numbers'
    listId = hubspot.lists.create_static_list(name)
    print('ok', listId)
    return


if __name__ == '__main__':
    main()
    print('main - done')