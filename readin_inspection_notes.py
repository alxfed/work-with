# -*- coding: utf-8 -*-
"""https://jsonlines.readthedocs.io/en/latest/
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting


def main():
    INPUT_FILE = '/home/alxfed/archive/inspections_notes_created.jl'
    created_notes = pd.read_json(INPUT_FILE, lines=True, dtype=object)

    # select what is useful
    inspection_notes = pd.DataFrame()
    inspection_notes['id'] = created_notes['id']
    inspection_notes['active'] = created_notes['active']
    inspection_notes['createdAt'] = created_notes['createdAt']
    inspection_notes['lastUpdated'] = created_notes['lastUpdated']
    inspection_notes['type'] = created_notes['type']
    inspection_notes['timestamp'] = created_notes['timestamp']
    inspection_notes['permit_'] = created_notes['permit']
    inspection_notes['insp_n'] = created_notes['insp_n']
    inspection_notes['insp_date'] = created_notes['insp_date']
    inspection_notes['insp_type'] = created_notes['insp_type']

    # upload the result to the home database
    conn_target = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    inspection_notes.to_sql(
        name=sorting.CREATED_INSPECTION_NOTES,
        con=conn_target, if_exists='replace', index=False)

    return


if __name__ == '__main__':
    main()
    print('main - done')
