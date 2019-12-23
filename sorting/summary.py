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

    def read_in(self, engagementId: str):
        # readin engagement
        result = ''
        if result:
            return True
        else:
            return False

    def add_content(self, **kwargs):
        self.content = ''
        return True

    def verify_content(self):
        # verification
        self.ready = True
        return self.ready

    def create(self):
        if self.ready:
            params = {'ownerId': SummaryNote.ownerId,
                      'timestamp': self.hs_timestamp,
                      'companyId': self.companyId,
                      'dealIds': self.deal_list,
                      'note': self.content}
            cre = hubspot.engagements.create_engagement_note(params)
            if cre:
                created_note = cre['engagement']
                self.engagementId = created_note['id']
                result = hubspot.companies.update_company(self.companyId, {'summary_note': self.engagementId,
                                     'summary_note_date': self.hs_timestamp})
                if result:
                    print('Created Summary Note: ', self.engagementId)
            pass
        else:
            print('Is not ready')
            return False

    def update(self, timestamp):
        if self.ready:
            params = {'timestamp': timestamp, 'note': self.content}
            res = hubspot.engagements.update_an_engagement(self.engagementId, params)
            # if res:
            #     print('updated the note ', inspection_note)
            #     # update the deal parameters last_inspection and last_inspection_date here
            #     result = hubspot.deals.update_a_deal_oauth(dealId, {
            #         'last_inspection': last_inspection_type.title(),
            #         'last_inspection_date': hubspot_timestamp,
            #         'insp_n': last_inspection_number})
            #     if result:
            #         print('Updated deal: ', dealId)
            #         return True
            # else:
            #     print('did not update the note', id)
            #     return False
        else:
            print('Is not ready')
            return False

    def prepare_note(self, **kwargs):
        self.ready      = False
        list_of_lines   = []

        if 'companyId' in kwargs.keys():
            self.companyId = kwargs['companyId']
        if self.companyId:
            self.deal_list = hubspot.associations.get_associations_oauth(self.companyId, '6')  # company to deals - full
            sleep(1)
        else:
            print('No company Id for the note. Nothing to prepare')
        for deal_n in self.deal_list:
            line = {}
            deal_data = deals_reference.loc[deals_reference['dealId'] == deal_n]
            # check the pipeline , dealstage , closedate , closed_won_reason , closed_lost_reason
            pipeline = deal_data['pipeline'].values[0]
            if pipeline == 'default':
                dealname = deal_data['dealname'].values[0]
                deal_readout = hubspot.deals.get_a_deal(deal_n)['properties']  # deal_n: int
                sleep(1)
                dealstage = deal_readout['dealstage']['value']
                dealstage_timestamp = deal_readout['dealstage']['timestamp']
                deal_owner = deal_readout['hubspot_owner_id']['value']
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
        # the list making cycle is over, time to format it
        if list_of_lines:
            to_sort = pd.DataFrame(list_of_lines)
            to_publish = pd.DataFrame()
            to_sort['date'] = pd.to_datetime(to_sort['date'], unit='ms')
            to_publish = to_sort.sort_values(by=['date'], ascending=False)
            to_publish['date'] = to_publish['date'].dt.strftime('%Y-%m-%d')
            self.content = to_publish.to_html(index=False) # the html parameters: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html?highlight=to_html#pandas.DataFrame.to_html
            self.ready = True

