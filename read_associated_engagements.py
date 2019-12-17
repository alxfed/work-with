# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import pandas as pd


def main():
    companyId = '1105532001' # Skender
    assoc_type = '2' # Company to contact, contact to company is 1
    # eng_list = hubspot.engagements.get_engagements_of_object(companyId)
    # engagements = pd.DataFrame(eng_list, dtype=object)
    associations_list = hubspot.associations.get_associations_oauth(companyId, assoc_type)
    vice_versa = hubspot.associations.get_associations_oauth(companyId, '1')
    # deal to contact is 3
    return


if __name__ == '__main__':
    main()
    print('main - done')