# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import pandas as pd


def main():
    contacts_list_file = '/home/alxfed/archive/downloaded_list.csv'
    cont_list = hubspot.lists.get_all_contacts_in('260')
    output = pd.DataFrame(cont_list)
    output.to_csv(contacts_list_file, index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')