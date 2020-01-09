"""
take a website name, split it and make an async request, searching
for all the emails in the domain.
"""
import pandas as pd
from tldextract import extract
import anymail
import sqlalchemy as sqlalc
import sorting


def main():
    # constants
    conn_source = sqlalc.create_engine(sorting.HOME_DATABASE_URI)
    conn_result = sqlalc.create_engine(sorting.PITCH_DATABASE_URI)

    companies = pd.read_sql_table(
        table_name=sorting.COMPANIES_TABLE, con=conn_source)

    created_companies = pd.DataFrame()

    companies_file_path = '/home/alxfed/archive/companies_downloaded.csv'
    output_file_path = '/home/alxfed/archive/verigoog_companies_with_emails.csv'

    # should be excluded
    # wordpress.com, houzz.com, yelp.com, facebook.com

    number = anymail.verify.credits()
    if number < 100:
        print('Low on credits in anymail')
    else:
        print('Number of credits ', number)

    # initiate the big objects

    name = companies['name']
    domain = companies['domain']
    result = anymail.find.emails(name, domain)
    chunk = pd.DataFrame(result)
    if not chunk.empty:
        chunk = chunk.astype(dtype=object)
        chunk.to_sql(name=sorting.FOUND_EMAILS_TABLE,
                     con=conn_result, if_exists='append', index=False)
        print('Added candidates of ', index)

    return


if __name__ == '__main__':
    main()
    print('main - done')


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