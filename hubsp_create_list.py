# -*- coding: utf-8 -*-
"""...
"""
import hubspot


def main():
    name = 'Test list created through the API'
    listId = hubspot.lists.create_static_list(name)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')