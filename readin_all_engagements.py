# -*- coding: utf-8 -*-
"""...
"""
import hubspot
import sqlalchemy as sqlalc
import sorting
import pandas as pd


def main():
    conn_result = sqlalc.create_engine(sorting.HOME_DATABASE_URI) # 'sqlite:////home/alxfed/dbase/home.sqlite'

    all_engagements, all_columns = hubspot.engagements.get_all_engagements_oauth()
    engagements = pd.DataFrame(data=all_engagements, columns=all_columns)
    del engagements['attachments']
    del engagements['metadata']
    # engagements = engagements.drop(['attachments', 'metadata'], axis=1)

    engagements.to_sql(name=sorting.ENGAGEMENTS_TABLE,
                       con=conn_result, if_exists='replace', index=False)
    return


if __name__ == '__main__':
    main()
    print('main - done')