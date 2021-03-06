# -*- coding: utf-8 -*-
"""...
"""
from . import constants
import pandas as pd
import sqlalchemy as sqlalc
import hubspot
import datetime as dt
import sorting
from time import sleep

conn = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
deals_reference = pd.read_sql_table(table_name=sorting.DEALS_TABLE, con=conn)



class SummaryNote(object):
    ownerId = '40202623' # Marfa Cabinets Data robot

    def __init__(self, **kwargs):
        if 'engagementId' in kwargs.keys(): self.engagementId = kwargs['engagementId']
        else: self.engagementId = ''
        if 'companyId' in kwargs.keys(): self.companyId = kwargs['companyId']
        else: self.companyId = ''
        if 'deal_list' in kwargs.keys(): self.deal_list = kwargs['deal_list']
        else: self.deal_list = []
        if 'content' in kwargs.keys(): self.content = kwargs['content']
        else: self.content = ''
        if 'hs_timestamp' in kwargs.keys(): self.hs_timestamp = kwargs['hs_timestamp']
        else: self.hs_timestamp = str(int(1000 * dt.datetime.now().timestamp()))
        self.ready = False

    def __del__(self): # just in case I will want to add the deletion of note here
        pass

    def create(self):
        if self.ready:
            params = {'ownerId': SummaryNote.ownerId,
                      'timestamp': self.hs_timestamp,
                      'companyId': self.companyId,
                      'dealIds': self.deal_list,
                      'note': self.content}
            cre = hubspot.engagements.create_engagement_note(params)
            if cre:
                sleep(1)
                created_note = cre['engagement']
                self.engagementId = created_note['id']
                result = hubspot.companies.update_company(self.companyId, {'summary_note_number': self.engagementId,
                                     'summary_note_date_str': self.hs_timestamp})
                if result:
                    print('Created new Summary Note: ', self.engagementId)
            pass
        else:
            print('Is not ready')
            return False

    def update(self):
        if self.ready:
            params = {'dealIds': self.deal_list, 'timestamp': self.hs_timestamp, 'note': self.content}
            res = hubspot.engagements.update_an_engagement(self.engagementId, params)
            if res:
                print('updated the note ', self.engagementId)
                # update the company parameters last_inspection and last_inspection_date here
                sleep(1)
                result = hubspot.companies.update_company(
                    self.companyId, {'summary_note_number': self.engagementId,
                                     'summary_note_date_str': self.hs_timestamp})
                if result:
                    print('Updated summary note on Company:  ', self.companyId)
                    return True
            else:
                print('did not update the note', self.engagementId)
                return False
        else:
            print('Note is not ready')
            return False

    def prepare_note(self, **kwargs):
        self.ready      = False
        list_of_lines   = []

        if 'companyId' in kwargs.keys():
            self.companyId = kwargs['companyId']
        if self.companyId:
            self.deal_list = hubspot.associations.get_associations_oauth(self.companyId, '6')  # company to deals - full
            sleep(1.5)
        else:
            print('No company Id for the note. Nothing to prepare')
        for deal_n in self.deal_list:
            line = {}
            deal_data = deals_reference.loc[deals_reference['dealId'] == deal_n]
            # check the pipeline , dealstage , closedate , closed_won_reason , closed_lost_reason
            if not deal_data.empty:
                pipeline = deal_data['pipeline'].values[0]
                if pipeline == 'default':
                    dealname = deal_data['dealname'].values[0]
                    deal_readout = hubspot.deals.get_a_deal(deal_n)['properties']  # deal_n: int
                    sleep(1.5)
                    if 'dealstage' in deal_readout.keys():
                        dealstage = deal_readout['dealstage']['value']
                        dealstage_timestamp = deal_readout['dealstage']['timestamp']
                    else:
                        dealstage = 'Unknown, probably deleted'
                        dealstage_timestamp = '1562462462247'
                    if 'hubspot_owner_id' in deal_readout.keys():
                        deal_owner = deal_readout['hubspot_owner_id']['value']
                    else:
                        deal_owner = 'Unknown'
                    # deal_amount = deal_data['amount'].values[0]
                    # closed_won_reason = deal_data['closed_won_reason']['value']
                    # closed_lost_reason = deal_data['closed_lost_reason']['value']
                    if dealstage in hubspot.NAMES_OF_STATES.keys():
                        stagename = hubspot.NAMES_OF_STATES[dealstage]
                    else:
                        stagename = 'Deleted stage type'
                    if deal_owner in hubspot.OWNERS_OF_IDS.keys():
                        ownername = hubspot.OWNERS_OF_IDS[deal_owner]
                    else:
                        ownername = 'Deactivated user'

                    line.update(
                        {'date': int(dealstage_timestamp), 'name': dealname,
                         'stage': stagename,
                         # 'amount': deal_amount,
                         'owner': ownername})
                    list_of_lines.append(line)
                else:
                    # pipeline is not 'default'
                    pass
            else:
                print('No deal in the data file', deal_n)
        # the list making cycle is over, time to format it
        if list_of_lines:
            to_sort = pd.DataFrame(list_of_lines)
            to_publish = pd.DataFrame()
            to_sort['date'] = pd.to_datetime(to_sort['date'], unit='ms')
            to_publish = to_sort.sort_values(by=['date'], ascending=False)
            to_publish['date'] = to_publish['date'].dt.strftime('%Y-%m-%d')
            self.content = to_publish.to_html(col_space=175, justify='left', index=False) # the html parameters: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html?highlight=to_html#pandas.DataFrame.to_html
            self.ready = True

