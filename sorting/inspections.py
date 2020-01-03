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
        if 'engagementId' in kwargs.keys(): self.engagementId = kwargs['engagementId'] # equat to 'insp_note'
        else: self.engagementId = ''
        if 'dealId' in kwargs.keys(): self.dealId = kwargs['dealId']
        else: self.dealId = ''
        if 'content' in kwargs.keys(): self.content = kwargs['content']
        else: self.content = ''
        self.ready = False
        if 'insp_n' in kwargs.keys(): self.insp_n = kwargs['insp_n']
        else: self.insp_n = ''
        if 'last_inspection' in kwargs.keys(): self.last_inspection = kwargs['last_inspection']
        else: self.last_inspection = ''
        if 'last_inspection_date' in kwargs.keys(): self.last_inspection_date = kwargs['last_inspection_date']
        else: self.last_inspection_date = None # dt.datetime(year=2019, month=7, day=12, hour=0, minute=0, second=0)
        if 'hs_timestamp' in kwargs.keys(): self.hs_timestamp = kwargs['hs_timestamp']
        else: self.hs_timestamp = ''

    def __del__(self): # just in case I will want to add the deletion of note here
        pass

    def create(self):
        if self.ready:
            params = {'ownerId': InspectionsNote.ownerId,
                      'timestamp': self.hs_timestamp,
                      'dealIds': [self.dealId],
                      'note': self.content}
            cre = hubspot.engagements.create_engagement_note(params)
            sleep(1)
            if cre:
                created_note = cre['engagement']
                self.engagementId = created_note['id']
                result = hubspot.deals.update_a_deal_oauth(
                    self.dealId, {'insp_note': self.engagementId,
                                  'insp_n': self.insp_n,
                                  'last_inspection': self.last_inspection,
                                  'last_inspection_date': self.last_inspection_date
                                  })
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
                    self.dealId, {'insp_note': self.engagementId,
                                  'insp_n': self.insp_n,
                                  'last_inspection': self.last_inspection,
                                  'last_inspection_date': self.last_inspection_date
                                  }) # TODO: datetime or string?
                if result:
                    print('Updated inspections note on Deal:  ', self.dealId)
                    return True
            else:
                print('did not update the note', self.engagementId)
                return False
        else:
            print('Note is not ready')
            return False

    def prepare_note(self, line, date, **kwargs):
        self.ready = False
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

        post_permit_inspections_table, last_inspection_line = post_permit_inspections(line, date, self.dealId)
        if not post_permit_inspections_table.empty:
            self.last_inspection_date = last_inspection_line['insp_date']
            # self.hs_timestamp = str(int(1000 * self.last_inspection_date.timestamp()))
            self.insp_n = last_inspection_line['insp_n']
            self.last_inspection = last_inspection_line['type_desc']
            self.hs_timestamp = int(1000 * self.last_inspection_date.timestamp()) # int(self.last_inspection_date.timestamp() * 1000)
            post_permit_inspections_table['insp_date'] = post_permit_inspections_table['insp_date'].dt.strftime(
                '%Y-%m-%d')
            post_permit_inspections_table.rename(columns={'insp_n': '#', 'insp_date': 'date', 'type_desc': 'type'}, inplace=True)
            self.content = post_permit_inspections_table.to_html(col_space=125, justify='left', header=True,
                                                              index=False)
            self.ready = True
            print('Thre are inspections after the permit for deal: ', self.dealId)
        else:
            print('No inspections after permit for deal: ', self.dealId)

'''

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

 last_inspection_number = last_inspection_line['insp_n']
            recorded_inspection = str(deal['insp_n'].values[0])
            inspection_note = str(deal['insp_note'].values[0])
            

         if list_of_lines:
            to_sort = pd.DataFrame(list_of_lines)
            to_publish = pd.DataFrame()
            to_sort['date'] = pd.to_datetime(to_sort['date'], unit='ms')
            to_publish = to_sort.sort_values(by=['date'], ascending=False)
            to_publish['date'] = to_publish['date'].dt.strftime('%Y-%m-%d')
            self.content = to_publish.to_html(col_space=175, justify='left', index=False) # the html parameters: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html?highlight=to_html#pandas.DataFrame.to_html
            self.ready = True

'''
