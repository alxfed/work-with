# -*- coding: utf-8 -*-
"""...
"""
HOME_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/home.sqlite'
SOURCE_DATABASE_URI = 'sqlite:////home/alxfed/dbase/home.sqlite'
TARGET_DATABASE_URI = 'sqlite:////home/alxfed/dbase/firstbase.sqlite'
PREP_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/thirdbase.sqlite'

LICENSED_GENERAL_CONTRACTORS_TABLE = 'all_licensed_general_contractors'
COMPANIES_TABLE = 'companies'
NEW_PERMITS_TABLE = 'new_permits'

OLD_COMPANIES_TABLE = 'old_companies'
NEW_COMPANIES_TABLE = 'new_companies'


def main():
    print('You have launched constants as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')