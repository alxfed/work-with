# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import sqlalchemy as sqlalc
import sorting
import hubspot
import datetime as dt

# constants
CLIENTS_COME_IN                     = '904851'
MAKE_QUOTE                          = '1112239'
DESIGN_ESTIMATE_REVISIONS           = 'fc1eda4f-23c1-4031-96da-eaadca9ab73e'
DESIGN_ESTIMATE_COMPLETED           = 'qualifiedtobuy'
QOUTE_READY_TO_BE_SENT              = '77a731b6-782c-4a38-a8b4-0a7b0d319d23'
QUOTE_SENT_OUT                      = '1175e2fb-5061-491e-81d6-65f0be6ce51e'
FOLLOW_UP_ON_QUOTE                  = '2cd78f67-7bfe-4691-824f-24dd4d33aff2'
SEND_OUT_TO_MEASURE                 = '7d4554f7-a7b9-4c69-a348-767f1aee7003'
FINAL_APPROVAL_BY_LEAD_DESIGNER     = '30fab7f0-4585-4d31-be27-7704fea2726b'
APPROVED_BY_LEAD_DESIGNER           = '92eede52-0557-4bfc-87cd-b8137889908c'
READY_FOR_CONTRACT                  = '1112240'
CLIENT_APPROVED                     = 'presentationscheduled'
CONTRACT_SENT_OUT                   = '1112241'
CONTRACT_SIGNED                     = 'decisionmakerboughtin'
DEPOSIT_COLLECTED                   = '87d11aa5-37df-4db0-b15d-975a172b34c4'
IN_PRODUCTION                       = 'contractsent'
PRODUCTION_FINISHED                 = '98866f99-d958-436c-89c5-2ee8d7d6d62d'
READY_FOR_DELIVERY                  = '1112276'
BALANCE_COLLECTED                   = '32ae2700-1937-4216-9c2c-0119a715ef17'
DELIVERY                            = 'closedwon'
PICK_UP                             = 'a8b2ecbf-f109-4d00-a813-92962430a892'
CLOSED_DELIVERED                    = 'closedlost'
LOST_NEVER_ORDERED                  = '825b606f-cda4-4a4c-a201-9bcf331a8aa3'

LIST_OF_STATES = ['904851', '1112239', 'fc1eda4f-23c1-4031-96da-eaadca9ab73e', 'qualifiedtobuy',
                  '77a731b6-782c-4a38-a8b4-0a7b0d319d23', '1175e2fb-5061-491e-81d6-65f0be6ce51e',
                  '2cd78f67-7bfe-4691-824f-24dd4d33aff2', '7d4554f7-a7b9-4c69-a348-767f1aee7003',
                  '30fab7f0-4585-4d31-be27-7704fea2726b', '92eede52-0557-4bfc-87cd-b8137889908c',
                  '1112240', 'presentationscheduled', '1112241', 'decisionmakerboughtin',
                  '87d11aa5-37df-4db0-b15d-975a172b34c4', 'contractsent',
                  '98866f99-d958-436c-89c5-2ee8d7d6d62d', '1112276', '32ae2700-1937-4216-9c2c-0119a715ef17',
                  'closedwon', 'a8b2ecbf-f109-4d00-a813-92962430a892', 'closedlost',
                  '825b606f-cda4-4a4c-a201-9bcf331a8aa3']

NAMES_OF_STATES = {'904851': 'Clients (come in)',
                   '1112239': 'Make quote',
                   'fc1eda4f-23c1-4031-96da-eaadca9ab73e': 'Design / Estimate / Revisions',
                   'qualifiedtobuy': 'Design / Estimates Completed',
                   '77a731b6-782c-4a38-a8b4-0a7b0d319d23': 'Quote, Ready to be Sent',
                   '1175e2fb-5061-491e-81d6-65f0be6ce51e': 'Quote sent out',
                   '2cd78f67-7bfe-4691-824f-24dd4d33aff2': 'Follow up on quote',
                   '7d4554f7-a7b9-4c69-a348-767f1aee7003': 'Send Out To Measure',
                   '30fab7f0-4585-4d31-be27-7704fea2726b': 'To be Checked for Final Approval by Lead Designer',
                   '92eede52-0557-4bfc-87cd-b8137889908c': 'Approved by Lead Designer',
                   '1112240': 'Ready For Contract',
                   'presentationscheduled': 'Client Approved',
                   '1112241': 'Contract Sent Out',
                   'decisionmakerboughtin': 'Contract Signed',
                   '87d11aa5-37df-4db0-b15d-975a172b34c4': 'Deposit Collected',
                   'contractsent': 'In Production',
                   '98866f99-d958-436c-89c5-2ee8d7d6d62d': 'Production Finished',
                   '1112276': 'Ready For Delivery',
                   '32ae2700-1937-4216-9c2c-0119a715ef17': 'Balance Collected',
                   'closedwon': 'Delivery',
                   'a8b2ecbf-f109-4d00-a813-92962430a892': 'Pick Up',
                   'closedlost': 'Closed / Delivered',
                   '825b606f-cda4-4a4c-a201-9bcf331a8aa3': 'Lost / Never Ordered'}


class SummaryNote(object):
    exist = False
    ready = False

    def __init__(self, **kwargs):
        if 'engagementId' in kwargs.keys():
            self.engagementId = kwargs['engagementId']
        if 'companyId' in kwargs.keys():
            self.companyId = kwargs['companyId']
        if 'deal_list' in kwargs.keys():
            self.deal_list = kwargs['deal_list']
        SummaryNote.exist = True

    def __del__(self):
        SummaryNote.exist = False

    def create(self):
        pass

    def update(self):
        if self.exist and self.ready:
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




def main():
    # 1. get a companyId from a deal;
    # 2. read summary_note and summary_note_date from this company;
    # 3. if should not be updated - terminate, if should - step 4.
    # 4. read associated engagements from this company;
    # 5. chech if it has been done already and if not - add filtered engagements to the _company_.
    conn_reference = sqlalc.create_engine(sorting.LOG_DATABASE_URI)
    deals = pd.read_sql_table(
        table_name=sorting.CREATED_DEALS_TABLE, con=conn_reference)

    for index, deal in deals.iterrows():
        dealId = deal['dealId']  # text format
        companyId = str(int(deal['companyId'])) # because it is FLOAT in the db

        deals_list = hubspot.associations.get_associations_oauth(companyId, '6') # company to deals - full
        engagements_list = hubspot.associations.get_associations_oauth(companyId, '7') # company to engagements - full
        eng_list = hubspot.engagements.get_engagements_of_object(companyId)
        for deal_n in deals_list:
            deal_data = hubspot.deals.get_a_deal(deal_n)['properties']
            # check the pipeline , dealstage , closedate , closed_won_reason , closed_lost_reason
            pipeline = deal_data['pipeline']['value']
            if pipeline == 'default':
                dealname = deal_data['dealname']['value']
                dealstage = deal_data['dealstage']['value']
                dealstage_timestamp = deal_data['dealstage']['timestamp']
                # closed_won_reason = deal_data['closed_won_reason']['value']
                # closed_lost_reason = deal_data['closed_lost_reason']['value']
                # if dealDate.empty:
                #     date = dt.datetime(year=2019, month=7, day=12, hour=0, minute=0, second=0)
                # else:
                #     date = dealDate.values[0]
                print('ok')
                # summary_note , summary_note_date
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
            else:
                # deal is not in the sales pipeline.
                pass
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