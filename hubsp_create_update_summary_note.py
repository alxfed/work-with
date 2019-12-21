# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot
import datetime as dt

# constants are in constants


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
        else:
            print('No company Id for the note. Nothing to prepare')
        for deal_n in self.deal_list:
            line = {}
            deal_data = hubspot.deals.get_a_deal(deal_n)['properties']  # deal_n: int
            # check the pipeline , dealstage , closedate , closed_won_reason , closed_lost_reason
            pipeline = deal_data['pipeline']['value']
            if pipeline == 'default':
                dealname = deal_data['dealname']['value']
                dealstage = deal_data['dealstage']['value']
                dealstage_timestamp = deal_data['dealstage']['timestamp']
                deal_owner = deal_data['hubspot_owner_id']['value']
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
                    {'date': int(dealstage_timestamp), 'name': dealname, 'stage': stagename, 'owner': ownername})
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


def main():
    # 1. get a companyId from a deal;
    # 2. read summary_note and summary_note_date from this company;
    # 3. if should not be updated - terminate, if should - step 4.
    # 4. read associated engagements from this company;
    # 5. chech if it has been done already and if not - add filtered engagements to the _company_.
    conn_reference = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.CREATED_DEALS_TABLE, con=conn_reference)

    companies = set() # unique companies also, see: https://stackoverflow.com/questions/10547343/add-object-into-pythons-set-collection-and-determine-by-objects-attribute

    for index, deal in deals.iterrows():
        dealId = deal['dealId']  # text format
        companyId = str(int(deal['companyId'])) # because it is FLOAT in the db
        if not companyId in companies:
            companies.add(companyId)
            co_info = hubspot.companies.get_company(companyId)
            if co_info:
                summary_note = ''
                co_properties = co_info['properties']
                if 'summary_note' in co_properties.keys():  # summary note exists
                    summary_note = co_properties['summary_note']['value']
                if summary_note:
                    summary_note_timestamp = co_properties['summary_note_date']['value']
                    now = int(1000 * dt.datetime.now().timestamp())
                    if (now - int(summary_note_timestamp)) > 10000:
                        old_note = SummaryNote(companyId=companyId,
                                               engagementId=summary_note,
                                               hs_timestamp=summary_note_timestamp)
                        old_note.prepare_note()
                        if old_note.ready:
                            res = old_note.update(timestamp=str(now))
                else:  # summary note doesn't exist
                    note = SummaryNote(companyId=companyId)
                    note.prepare_note()
                    if note.ready:
                        res = note.create()
                    else:
                        print('Note is empty')
            else:
                # no company info. what kind of a company is that?
                # Somethin's not working properly. Stop!
                print('Company not found')
        else:
            # company has been processed.
            print('One more deal of:  ', companyId)
    return


if __name__ == '__main__':
    main()
    print('main - done')


'''
'hs_object_id': 
    {'value': '436812705', 
    'timestamp': 1545070632884, 
    'source': 'CALCULATED', 
    'sourceId': None, 
    'versions': [{'name': 'hs_object_id', 'value': '436812705', 'timestamp': 1545070632884, 'source': 'CALCULATED', 'sourceVid': []}]
    }, 
'hs_analytics_source_data_2': 
    {'value': 'CRM_UI', 
    'timestamp': 1557852770795, 
    'source': 'DEALS', 
    'sourceId': 'deal sync triggered by company id=1114608131', 
    'versions': [{'name': 'hs_analytics_source_data_2', 'value': 'CRM_UI', 'timestamp': 1557852770795, 'sourceId': 'deal sync triggered by company id=1114608131', 'source': 'DEALS', 'sourceVid': []}]
    }, 
'hs_analytics_source_data_1': 
    {'value': 'CONTACTS', 
    'timestamp': 1557852770795, 
    'source': 'DEALS', 'sourceId': 
    'deal sync triggered by company id=1114608131', 
    'versions': [{'name': 'hs_analytics_source_data_1', 'value': 'CONTACTS', 'timestamp': 1557852770795, 'sourceId': 'deal sync triggered by company id=1114608131', 'source': 'DEALS', 'sourceVid': []}]}
    },
'imports': [], 
'stateChanges': []
'''

'''
                    post_permit_inspections_table, last_inspection_table = post_permit_inspections(line, date, dealId)
                    if not post_permit_inspections_table.empty:
                        last_inspection_number = last_inspection_table['insp_n']
                        recorded_inspection = str(deal['insp_n'].values[0])
                        inspection_note = str(deal['insp_note'].values[0])
                        if not last_inspection_number == recorded_inspection:
                            last_inspection_date = last_inspection_table['insp_date']
                            last_inspection_type = last_inspection_table['type_desc']
                            hubspot_timestamp = int(last_inspection_date.timestamp() * 1000)
                            post_permit_inspections_table['insp_date'] = post_permit_inspections_table['insp_date'].dt.strftime('%Y-%m-%d')
                            note_text = post_permit_inspections_table.to_html(header=False, index=False)
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
                                params = {'ownerId': ownerId, 'timestamp': hubspot_timestamp, 'dealId': dealId, 'note': note_text}
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

'''