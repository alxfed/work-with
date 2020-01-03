# -*- coding: utf-8 -*-
"""Inspections note object
"""
from . import constants
import pandas as pd
import sqlalchemy as sqlalc
import hubspot
import datetime as dt
import sorting
from time import sleep


class InspectionsNote(object):
    ownerId = '40202623' # Marfa Cabinets Data robot

    def __init__(self, **kwargs):
        if 'engagementId' in kwargs.keys(): self.engagementId = kwargs['engagementId']
        else: self.engagementId = ''
        if 'dealId' in kwargs.keys(): self.dealId = kwargs['dealId']
        else: self.dealId = ''
        if 'content' in kwargs.keys(): self.content = kwargs['content']
        else: self.content = ''
        if 'hs_timestamp' in kwargs.keys(): self.hs_timestamp = kwargs['hs_timestamp']
        else: self.hs_timestamp = str(int(1000 * dt.datetime.now().timestamp()))
        self.ready = False

    def __del__(self): # just in case I will want to add the deletion of note here
        pass

    def create(self):
        if self.ready:
            params = {'ownerId': InspectionsNote.ownerId,
                      'timestamp': self.hs_timestamp,
                      'dealIds': [self.dealId],
                      'note': self.content}
            cre = hubspot.engagements.create_engagement_note(params)
            if cre:
                sleep(1)
                created_note = cre['engagement']
                self.engagementId = created_note['id']
                result = hubspot.deals.update_a_deal_oauth(self.dealId, {'summary_note_number': self.engagementId,
                                     'summary_note_date_str': self.hs_timestamp})
                if result:
                    print('Created new Summary Note: ', self.engagementId)
            pass
        else:
            print('Is not ready')
            return False

    def update(self):
        if self.ready:
            params = {'dealIds': [self.dealId], 'timestamp': self.hs_timestamp, 'note': self.content}
            res = hubspot.engagements.update_an_engagement(self.engagementId, params)
            if res:
                print('updated the note ', self.engagementId)
                # update the company parameters last_inspection and last_inspection_date here
                sleep(1)
                result = hubspot.deals.update_a_deal_oauth(
                    self.dealId, {'summary_note_number': self.engagementId,
                                     'summary_note_date_str': self.hs_timestamp})
                if result:
                    print('Updated summary note on Company:  ', self.dealId)
                    return True
            else:
                print('did not update the note', self.engagementId)
                return False
        else:
            print('Note is not ready')
            return False

    def prepare_note(self, line, date, **kwargs):

        # post permit inspections
        def post_permit_inspections(scraped_line, date, dealId):
            inspections_table = pd.DataFrame()
            last_inspection = pd.DataFrame()
            insp_table = pd.DataFrame.from_records(scraped_line['insp_table'])
            if not insp_table.empty:  # any inspections at all in this record? Otherwise - why bother?
                if 'insp_date' in insp_table.keys():  # there is a table and it has 'insp_date' column
                    insp_table['insp_date'] = pd.to_datetime(insp_table['insp_date'], infer_datetime_format=True)
                    inspections_table = insp_table[insp_table['insp_date'] >= date]
                    if not inspections_table.empty:
                        last_inspection = inspections_table.iloc[0]
                    else:
                        print('No inspections after permit for deal', dealId)
                else:  # there is an ispection with number but no date column? Really?
                    pass
            else:  # inspections table is empty
                pass
            return inspections_table, last_inspection

        self.ready = False

        post_permit_inspections_table, last_inspection_line = post_permit_inspections(line, date, self.dealId)
        if not post_permit_inspections_table.empty:
            last_inspection_number = last_inspection_line['insp_n']
            recorded_inspection = str(deal['insp_n'].values[0])
            inspection_note = str(deal['insp_note'].values[0])
            if not last_inspection_number == recorded_inspection:
                last_inspection_date = last_inspection_line['insp_date']
                last_inspection_type = last_inspection_line['type_desc']
                hubspot_timestamp = int(last_inspection_date.timestamp() * 1000)
                post_permit_inspections_table['insp_date'] = post_permit_inspections_table['insp_date'].dt.strftime(
                    '%Y-%m-%d')
                post_permit_inspections_table.rename(columns={'insp_n': '#', 'insp_date': 'date', 'type_desc': 'type'})
                note_text = post_permit_inspections_table.to_html(col_space=125, justify='left', header=True,
                                                                  index=False)
                # branching for existent and non-existent - here
                if inspection_note:
                    params = {'timestamp': hubspot_timestamp, 'note': note_text}
                    res = hubspot.engagements.update_an_engagement(inspection_note, params)
                    if res:
                        print('updated the note ', inspection_note)
                        # update the deal parameters last_inspection and last_inspection_date here
                        result = hubspot.deals.update_a_deal_oauth(dealId, {
                            'last_inspection': last_inspection_type.title(),
                            'last_inspection_date': hubspot_timestamp,
                            'insp_n': last_inspection_number})
                        if result:
                            print('Updated deal: ', dealId)
                    else:
                        print('did not update the note', id)
                else:
                    params = {'ownerId': ownerId, 'timestamp': hubspot_timestamp, 'dealIds': [dealId],
                              'note': note_text}
                    cre = hubspot.engagements.create_engagement_note(params)
                    if cre:
                        created_note = cre['engagement']
                        inspection_note = created_note['id']
                        result = hubspot.deals.update_a_deal_oauth(dealId, {'insp_note': inspection_note,
                                                                            'insp_n': last_inspection_number,
                                                                            'last_inspection': last_inspection_type.title(),
                                                                            'last_inspection_date': hubspot_timestamp})
                        if result:
                            print('Updated deal: ', dealId)
                note = pd.DataFrame()
                # note.to_sql(name=sorting.INSPECTION_NOTES,
                #             con=conn_result, if_exists='append', index=False)
            else:
                print('The last inspection number is the same. No new inspections. Nothing to update.')
        else:
            print('No inspections after permit for deal: ', dealId)

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
