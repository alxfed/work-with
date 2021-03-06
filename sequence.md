### The sequence:
1. Set the start and end dates in <br>
**readin_new_permits.py** and run it. Stores:<br>
**home**.sqlite table **'new_permits'**<br>
<br>
2. **sort_new_permits.py**<br>
finds the general contractors and stores<br>
**firstbase**.sqlite table **'new_permits_with_gen_contractors'**<br>
<br>
3. **readin_all_companies.py**<br>
creates an actual table of companies in:<br>
**home**.sqlite table **'companies'**<br>
<br>
4. **sort_companies.py**<br>
sorts the general contractors of new permits<br>
against the **home**.sqlite **'companies'** that are in the system<br>
and **home**.sqlite table **'all_licensed_general_contractors'**.<br>
Creates:<br>
a.) **secondbase**.sqlite table **'new_companies'**;<br>
b.) **thirdbase**.sqlite table **'old_companies_permits'**<br>
c.) **thirdbase**.sqlite table **'not_found'** (general contractors)<br><br>
5. **create_new_companies.py**<br>
creates the **secondbase**.sqlite table **'new_companies'**<br>
in HubSpot<br><br>
6. repeat 3 and 4 one more time.<br>
**TODO:** erase old records from 'new_companies' when the result<br>
of sorting is empty<br><br>
7. **hubsp_create_deals.py**<br>
creates deals for **thirdbase**.sqlite table **'old_companies_permits'**<br>
(and automatically assiciates them with the companies during the creation)<br>
records the log to:<br>
**logbase**.sqlite table **'created_deals'**<br><br>
8. **readin_all_deals.py**<br>
updates the **home**.sqlite table **'deals'**<br><br>
9. **hubsp_add_associated_contacts_to_deal.py**<br>
uses **logbase**.sqlite table **'created_deals'** and<br>
_**reads**_ the current associations of the company.<br><br>
10. **create_update_all_summary_notes.py**<br><br>



