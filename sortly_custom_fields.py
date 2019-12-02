# -*- coding: utf-8 -*-
"""Read the custom fields
"""
import sortly


def main():
    response, headers = sortly.list.custom_fields()
    # 'Sortly-Rate-Limit-Max': '1000',
    # 'Sortly-Rate-Limit-Remaining': '999',
    # 'Sortly-Rate-Limit-Reset': '814'
    print(headers)
    print('ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')