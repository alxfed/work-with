# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import hubspot


def main():
    output_file_path = '/home/alxfed/archive/lists_downloaded.csv'
    list_of_lists, output_columns = hubspot.lists.get_all_lists_oauth()
    output = pd.DataFrame(list_of_lists, columns=output_columns, dtype=object)
    output.to_csv(output_file_path, index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')