# -*- coding: utf-8 -*-
"""...
"""
from itertools import islice


def main():
    list = ['123', '232', '345', '456', '345']
    chunk_list = [list[i:i + 3] for i in range(0, len(list), 3)]
    print('ok')
    for i in slice:
        print('ok', i)
    return


if __name__ == '__main__':
    main()
    print('main - done')