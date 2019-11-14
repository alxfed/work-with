# -*- coding: utf-8 -*-
"""...
"""
import verigoog
import pandas as pd


def main():
    downloaded_licensed_general_contractors = '/home/alxfed/archive/downloaded-licensed-general-contractors.csv'
    all_columns = ['Company ID', 'Last Modified Date', 'Lead Status',
                   'Total Revenue', 'Postal Code', 'Twitter Followers',
                   'Company Domain Name', 'Last Touch Converting Campaign',
                   'First Touch Converting Campaign', 'Recent Deal Close Date',
                   'Number of Pageviews', 'Number of Employees',
                   'Last Meetings Tool Submission Campaign', 'Phone Unidentified',
                   'Time of Last Session', 'Time of First Session', 'Close Date',
                   'Facebook Fans', 'Associated Deals', 'Recent Deal Amount',
                   'Number of times contacted', 'First Conversion Date',
                   'Original Source Type', 'First Deal Created Date',
                   'Number of Form Submissions', 'Last Meetings Tool Submission Medium',
                   'Facebook Company Page', 'Create Date', 'LinkedIn Bio',
                   'First Conversion', 'Last Meetings Tool Submission', 'City', 'Name',
                   'Number of child companies', 'Phone Toll', 'Number of Sessions',
                   'Phone Number', 'Company owner', 'Phone Contact', 'Phone Landline',
                   'About Us', 'Last Activity Date', 'Next Activity Date',
                   'Last Meetings Tool Submission Source', 'Owner Assigned Date',
                   'State/Region', 'Phone VoIP', 'Email address',
                   'LinkedIn Company Page', 'Total Money Raised', 'Phone Mobile',
                   'Associated Contacts', 'Original Source Data 1', 'Target Account',
                   'Recent Conversion Date', 'Original Source Data 2',
                   'Lifecycle Stage', 'Last Contacted', 'Street Address',
                   'Recent Conversion', 'HubSpot Team', 'Twitter Bio',
                   'Web Technologies', 'Country/Region', 'First Contact Create Date',
                   'Time Zone', 'Time Last Seen', 'Time First Seen', 'Type',
                   'Website URL', 'Year Founded', 'Twitter Handle', 'Google Plus Page',
                   'Days to Close', 'Description', 'Annual Revenue', 'Parent Company',
                   'Category', 'Industry', 'Street Address 2', 'Is Public',
                   'Associated Company ID', 'Associated Company']
    licensed_in_the_system = pd.read_csv(downloaded_licensed_general_contractors, dtype=object)

    for index, contractor in licensed_in_the_system.iterrows():
        name = contractor['Name']
        companyId = contractor['Company ID']
        # text search with the help of find_place and bias, then place details for every candidate
        result = verigoog.places.find_in_chicago(name)
        # search with text query, within a radius from a location with given type filtering
        other_result = verigoog.places.of_type_in_chicago(name, 'general_contractor')
        print(result, '\n', other_result)
    return


if __name__ == '__main__':
    main()
    print('main - done')


'''
'place_id': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'plus_code': {'compound_code': '7P88+JW Coal City, Illinois', 'global_code': '86HH7P88+JW'}, 
'rating': 3.5, 
'reference': 'ChIJixEoCtUpDIgRke3x5nWfa54', 
'types': ['general_contractor', 'point_of_interest', 'establishment']
'''