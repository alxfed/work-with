# -*- coding: utf-8 -*-
"""...
"""
import sqlalchemy
import pandas as pd


def filter_out_known_companies(data):
    new = pd.DataFrame()
    old = pd.DataFrame()
    return new, old


def filter_out_big_ra_and_nce(data):
    big_nc = pd.DataFrame()
    big_ra = pd.DataFrame()
    return big_nc, big_ra


def general_contractors_and_permits(data):
    output_list = []
    for row_n, row in data.iterrows():
        for n in range(14):
            contact_number = str(n + 1)
            con_type_key = f'contact_{contact_number}_type'
            if con_type_key in row.keys():
                contact_type = row[con_type_key]
                if contact_type == 'CONTRACTOR-GENERAL CONTRACTOR':
                    line = {'name':             row[f'contact_{contact_number}_name'],
                            'city':             row[f'contact_{contact_number}_city'],
                            'state':            row[f'contact_{contact_number}_state'],
                            'zip':              row[f'contact_{contact_number}_zipcode'],
                            'permit_':          row['permit_'],
                            'permit_type':      row['permit_type'],
                            'issue_date':       row['issue_date'],
                            'work_description': row['work_description'],
                            'street_number':    row['street_number'],
                            'street_direction': row['street_direction'],
                            'street_name':      row['street_name'],
                            'suffix':           row['suffix'],
                            'reported_cost':    row['reported_cost']
                            }
                    output_list.append(line)
                    # print(line)
            else:
                break

    general_contractors = pd.DataFrame(output_list)
    return general_contractors


def compare_with_companies_and_reference(row, present, reference):
    # reference - licensed general contractors in the official list
    # present - companies in the system
    # row - permit
    permit_to_add = pd.DataFrame()
    permit_not_to_add = pd.DataFrame()
    company_to_add = pd.DataFrame()
    not_found = pd.DataFrame()

    co_name, sep, dba  = row['name'].partition(' Dba ')  # split if there is a dba, then sep and dba are nonzero
    # va = present['name'].values
    found = present[present['name'].str.find(sub=co_name) != -1]
    if found.empty:
        found_in_reference = reference[reference['company_name'].str.find(sub=co_name) != -1]
        if not found_in_reference.empty:
            company_to_add = company_to_add.append(found_in_reference)
        else:
            print('Did not find ', row['name'], ' in the list of licensed general contractors')
            print('Adding it to the not_found table \n')
            pass
    else:
        permit_to_add = permit_to_add.append(row)
        permit_to_add['companyId'] = found['companyId'].values[0]
        pass

    return permit_to_add, company_to_add, permit_not_to_add, not_found


def main():
    print('You have launched companies.py as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')