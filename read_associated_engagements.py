# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import pandas as pd


def main():
    companyId = '1105532001' # Skender
    assoc_type = '2' # Company to contact, contact to company is 1
    # eng_list = hubspot.engagements.get_engagements_of_object(companyId)
    # engagements = pd.DataFrame.from_records(eng_list)
    associations_list = hubspot.associations.get_associations_oauth(companyId, assoc_type)
    return


if __name__ == '__main__':
    main()
    print('main - done')