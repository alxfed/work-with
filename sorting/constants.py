# -*- coding: utf-8 -*-
"""...
"""
HOME_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/home.sqlite'
SOURCE_DATABASE_URI = 'sqlite:////home/alxfed/dbase/home.sqlite'
TARGET_DATABASE_URI = 'sqlite:////home/alxfed/dbase/firstbase.sqlite'
INTERM_DATABASE_URI = 'sqlite:////home/alxfed/dbase/secondbase.sqlite'
PREP_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/thirdbase.sqlite'

LICENSED_GENERAL_CONTRACTORS_TABLE = 'all_licensed_general_contractors'
COMPANIES_TABLE = 'companies'

NEW_PERMITS_TABLE = 'new_permits'
NEW_PERMITS_WITH_GENERAL_CONTRACTORS_TABLE = 'new_permits_with_gen_contractors'

GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE = 'gen_contractors_from_new_permits'
UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE = 'unique_gen_contractors_from_new_permits'

OLD_COMPANIES_TABLE = 'old_companies'
OLD_COMPANIES_PERMITS_TABLE = 'old_companies_permits'
NEW_COMPANIES_TABLE = 'new_companies'
NEW_COMPANIES_PERMITS_TABLE = 'new_companies_permits'

CREATED_COMPANIES_TABLE = 'created_companies'


def main():
    print('You have launched constants as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')