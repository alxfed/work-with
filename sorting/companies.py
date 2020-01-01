# -*- coding: utf-8 -*-
"""...
"""
import pandas as pd
import re
import comparison


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
                    # Debug for particular company
                    # debug_company_name = 'Mk Construction'
                    # debug_company = row[f'contact_{contact_number}_name'].title()
                    # if debug_company_name in debug_company:
                    #     print('ok')
                    #     # question = input(debug_company +' y/n? ')
                    #     # if question.startswith('y'):
                    #     #     print('You saw it')
                    #     # else:
                    #     #     print('You saw it anyway...')
                    # Debug for particular company
                    line = {'name':             row[f'contact_{contact_number}_name'].title(),
                            'city':             row[f'contact_{contact_number}_city'].title(),
                            'state':            row[f'contact_{contact_number}_state'],
                            'zip':              row[f'contact_{contact_number}_zipcode'],
                            'permit_':          row['permit_'],
                            'permit_type':      row['permit_type'],
                            'issue_date':       row['issue_date'],
                            'work_description': row['work_description'],
                            'street_number':    row['street_number'],
                            'street_direction': row['street_direction'],
                            'street_name':      row['street_name'].title(),
                            'suffix':           row['suffix'],
                            'reported_cost':    row['reported_cost']
                            }
                    output_list.append(line)
                    # print(line)
            else:
                break

    general_contractors = pd.DataFrame(output_list)
    return general_contractors


def compare_company_with_existing_and_reference(company, present, reference):
    # reference - licensed general contractors in the official list
    # present - companies in the system
    # company - verigooged or other company
    new_company = pd.DataFrame()
    old_company_and_corrections = pd.DataFrame()
    not_found = pd.DataFrame()


def compare_permit_with_companies_and_reference(row, present, reference):
    # reference - licensed general contractors in the official list
    # present - companies in the system
    # row - permit
    permit_to_add = pd.DataFrame()
    company_to_add = pd.DataFrame()
    not_found = pd.DataFrame()

    co_name, sep, dba  = row['name'].partition(' Dba ')  # split if there is a dba, then sep and dba are nonzero
    # va = present['name'].values
    co_name = co_name.strip()
    co_name = re.sub('[,.]', '', co_name)
    present['name'] = present['name'].str.replace(r'[,.]', '')
    found = present[present['name'].str.find(sub=co_name) != -1]
    if found.empty:
        ref = reference.copy()
        ref['company_name'] = reference['company_name'].str.replace(r'[,.]', '')
        found_in_reference = ref[ref['company_name'].str.contains(co_name)]
        if not found_in_reference.empty:
            row_n = found_in_reference.index[0]
            company_to_add = company_to_add.append(reference.iloc[[row_n]])
        else:
            not_found = not_found.append(row)
    else:
        permit_to_add = permit_to_add.append(row)
        permit_to_add['companyId'] = found['companyId'].values[0]
    return permit_to_add, company_to_add, not_found

    # Debug for particular company
    # debug_company_name = 'Mk Construction'
    # debug_company = co_name
    # if debug_company_name in debug_company:
    #     print('ok')
    # Debug for particular company


def main():
    print('You have launched companies.py as __main__')
    return


if __name__ == '__main__':
    main()
    print('main - done')