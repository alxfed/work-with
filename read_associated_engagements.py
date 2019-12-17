# -*- coding: utf-8 -*-
"""...
"""
import hubspot


def main():
    companyId = '1105532001' # Skender
    eng_list = hubspot.engagements.get_engagements_of_object(companyId)
    return


if __name__ == '__main__':
    main()
    print('main - done')