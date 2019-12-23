# -*- coding: utf-8 -*-
"""...
"""
HOME_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/home.sqlite'
SOURCE_DATABASE_URI = 'sqlite:////home/alxfed/dbase/home.sqlite'

TARGET_DATABASE_URI = 'sqlite:////home/alxfed/dbase/firstbase.sqlite'
INTERM_DATABASE_URI = 'sqlite:////home/alxfed/dbase/secondbase.sqlite'
PREP_DATABASE_URI   = 'sqlite:////home/alxfed/dbase/thirdbase.sqlite'

PITCH_DATABASE_URI  = 'sqlite:////home/alxfed/dbase/center.sqlite'

LOG_DATABASE_URI    = 'sqlite:////home/alxfed/dbase/logbase.sqlite'

LICENSED_GENERAL_CONTRACTORS_TABLE                  = 'all_licensed_general_contractors'
NOT_FOUND_GENERAL_CONTRACTORS_TABLE                 = 'not_found_general_contractors'
GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE          = 'gen_contractors_from_new_permits'
UNIQUE_GENERAL_CONTRACTORS_FROM_NEW_PERMITS_TABLE   = 'unique_gen_contractors_from_new_permits'

COMPANIES_TABLE             = 'companies'
OLD_COMPANIES_TABLE         = 'old_companies'
OLD_COMPANIES_PERMITS_TABLE = 'old_companies_permits'
NEW_COMPANIES_TABLE         = 'new_companies'
NEW_COMPANIES_PERMITS_TABLE = 'new_companies_permits'
CREATED_COMPANIES_TABLE     = 'created_companies'

CREATED_SUMMARY_NOTES       = 'created_summary_notes'
SUMMARY_NOTES               = 'summary_notes'
UPDATED_SUMMARY_NOTES       = 'updated_summary_notes'

DEALS_TABLE                 = 'deals'
THOSE_DEALS_TABLE           = 'those_deals'
DEALS_WITH_ALL_PARAMS_TABLE = 'deals_everything'
CREATED_DEALS_TABLE         = 'created_deals'
FRESH_DEALS_TABLE           = 'fresh_deals'

CREATED_INSPECTION_NOTES    = 'created_insp_notes'
INSPECTION_NOTES            = 'inspection_notes_log'
ENGAGEMENTS_TABLE           = 'all_engagements'

NEW_PERMITS_TABLE           = 'new_permits'
NEW_PERMITS_WITH_GENERAL_CONTRACTORS_TABLE = 'new_permits_with_gen_contractors'


def main():
    print('You have launched constants as main')
    return


if __name__ == '__main__':
    main()
    print('main - done')