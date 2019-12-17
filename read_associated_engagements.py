# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import pandas as pd


def main():
    companyId = '1105532001' # Skender
    eng_list = hubspot.engagements.get_engagements_of_object(companyId)
    engagements = pd.DataFrame.from_records(eng_list)
    return


if __name__ == '__main__':
    main()
    print('main - done')