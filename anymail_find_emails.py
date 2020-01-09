"""
take a website name, split it and make an async request, searching
for all the emails in the domain.
"""
import pandas as pd
import anymail
import sqlalchemy as sqlalc
import sorting


def main():
    # constants
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_result = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_source)

    # verify credits
    number = anymail.verify.credits()
    if number < 100:
        print('Low on credits in anymail')
    else:
        print('Number of credits ', number)

    # cycle over the list and find emails
    for index, company in companies.iterrows():
        if company['elgoog_place_id']:
            name = company['name']
            domain = company['domain']
            if domain:
                result = anymail.find.emails(name, domain)
                if result: # record the found emails
                    chunk = pd.DataFrame(result, index=[index])
                    chunk['companyId'] = company['companyId']
                    chunk.reindex(index=['companyId', 'name', 'domain', 'emails', 'email_class'])
                    chunk.to_sql(name=sorting.FOUND_EMAILS_TABLE,
                                 con=conn_result, if_exists='append', index=False)
                    print('Added emails of company', name, '\n\n')
                else:
                    print('Did not add anythong for  ', name, '  timeout')
        else:
            pass
    return


if __name__ == '__main__':
    main()
    print('done')


'''
with open(file_path) as f:
    f_csv = csv.DictReader(f, restkey='Rest', restval='')
    with open(output_file_path, 'w') as wr:
        wr_csv = csv.DictWriter(wr, fieldnames=fieldnames)
        wr_csv.writeheader()
        for row in f_csv:
            website = row['Website']
            if not website:  # check whether there is a website
                pass
            else:
                tsd, td, tsu = extract(website)  # tldextract
                payload = {'domain': td + '.' + tsu,
                           'company_name': row['Name']}
                r = requests.post(api_url, headers=headers,
                                  json=payload, timeout=60)
                if r.status_code > 202:
                    """errors
                    """
                    whats_up = r.json()
                    print('Wow! Errors happen!', r.status_code, whats_up['error'])
                    pass
                elif r.status_code < 203:
                    timeout = False; attempts = 0
                    while r.status_code != 200:
                        time.sleep(3)
                        r = requests.request('POST', api_url,
                                             headers=headers, json=payload)
                        if r.status_code == 200:
                            break
                        else:
                            attempts += 1
                            print(attempts)
                            if attempts > 10:
                                timeout = True
                                break
                    if not timeout:
                        resp = r.json()
                        row.update({'emails': " ".join(resp['emails'])})
                        row.update({'email_class': resp['email_class']})
                        print(row['Name'], row['emails'], row['email_class'])
                    else:
                        print(row['Name'], 'Timeout')
                else:
                    print('I dunno what this is...', r.status_code)
                    pass
            wr_csv.writerow(row)
            rows.append(row)

with open(final_file_path,'w') as f:
    f_csv = csv.DictWriter(f, fieldnames=fieldnames)
    f_csv.writeheader()
    f_csv.writerows(rows)

print('OK')
'''