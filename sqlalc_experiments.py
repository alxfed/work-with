# -*- coding: utf-8 -*-
"""...
"""
from sqlalchemy import *
from datetime import datetime

def main():
    metadata = MetaData('sqlite:////home/alxfed/dbase/exper.sqlite')

    user_table = Table(
        'tf_user', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_name', Unicode(16),
               unique=True, nullable=False),
        Column('password', Unicode(40), nullable=False),
        Column('display_name', Unicode(255), default=''),
        Column('created', DateTime, default=datetime.now))

    group_table = Table(
        'tf_group', metadata,
        Column('id', Integer, primary_key=True),
        Column('group_name', Unicode(16),
               unique=True, nullable=False))

    permission_table = Table(
        'tf_permission', metadata,
        Column('id', Integer, primary_key=True),
        Column('permission_name', Unicode(16),
               unique=True, nullable=False))

    user_group_table = Table(
        'tf_user_group', metadata,
        Column('user_id', None, ForeignKey('tf_user.id'),
               primary_key=True),
        Column('group_id', None, ForeignKey('tf_group.id'),
               primary_key=True))

    group_permission_table = Table(
        'tf_group_permission', metadata,
        Column('permission_id', None, ForeignKey('tf_permission.id'),
               primary_key=True),
        Column('group_id', None, ForeignKey('tf_group.id'),
               primary_key=True))

    metadata.create_all()
    metadata.bind.echo = True
    # insert statement executed multiple times
    stmt = user_table.insert()

    stmt.execute(user_name='rick', password='secret',
                 display_name='Rick Copeland')
    stmt.execute(user_name='rick1', password='secret',
                 display_name='Rick Copeland Clone')
    # select statement executed multiple times
    stmt = user_table.select()
    result = stmt.execute()
    for row in result:
        print(row)
    return


if __name__ == '__main__':
    main()
    print('main - done')

'''
table_name = 'companies'
    meta = MetaData(connection)
    meta.reflect(only=[table_name], views=True)
    companies = pd.read_sql_table(table_name=table_name, con=connection)
    licensed_gen_contractors = pd.read_sql_table(table_name='licensed_general_contractors', con=connection)
    licensed_gen_contractors = licensed_gen_contractors.fillna('')
'''

