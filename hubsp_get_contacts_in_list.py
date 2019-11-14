# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import pandas as pd


def main():
    cont_list = hubspot.lists.get_all_contacts_in('260')
    return


if __name__ == '__main__':
    main()
    print('main - done')