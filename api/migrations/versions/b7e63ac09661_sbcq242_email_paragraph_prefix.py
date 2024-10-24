"""sbcq242_email_paragraph&prefix

Revision ID: b7e63ac09661
Revises: d56650c6d5b8
Create Date: 2024-10-10 10:38:01.184171

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'b7e63ac09661'
down_revision = 'd56650c6d5b8'
branch_labels = None
depends_on = None


def upgrade():

    # Generated SQL commands for upgrade
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
- Jurisdiction and Roll Number of Property 
- Your Property Address
- Valid Photo ID (BC Drivers Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
- Your Social Insurance Number 
- Property Taxation Notice (helpful not required)

Please Note: SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply' WHERE service_id = '94';""")
    op.execute("""UPDATE service SET email_paragraph = NULL WHERE service_id = '166';""")
    op.execute("""UPDATE service SET email_paragraph = NULL WHERE service_id = '169';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
- ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
- How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
- What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx' WHERE service_id = '304';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
- ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp 
- Getting your Learners Licence: https://www.icbc.com/driver-licensing/new-drivers/Pages/Get-your-L.aspx 
- Getting your Commercial Licence: https://www.icbc.com/driver-licensing/types-licences/Pages/Get-your-commercial-driver-licence.aspx 
- What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx' WHERE service_id = '313';""")
    op.execute("""UPDATE service SET online_link = 'https://justice.gov.bc.ca/cannabislicensing/policy-document/worker-qualification-home' WHERE service_id = '507';""")
    op.execute("""UPDATE service SET prefix = 'B' WHERE service_id = '554';""")
    op.execute("""UPDATE service SET email_paragraph = '' WHERE service_id = '572';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
- Jurisdiction and Roll Number of Property 
- Your Property Address
- Valid Photo ID (BC Drivers Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
- Your Social Insurance Number 
- Municipal Property Taxation Notice (helpful not required)

Please Note:  SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply' WHERE service_id = '916';""")
    op.execute("""UPDATE service SET online_link = 'https:\\www2.gov.bc.ca/getvaccinated.html' WHERE service_id = '984';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
- ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
- How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
- What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx' WHERE service_id = '1125';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1279';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1285';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1288';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1290';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1291';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1292';""")
    op.execute("""UPDATE service SET prefix = 'A' WHERE service_id = '1293';""")
    op.execute("""UPDATE service SET service_code = 'Other - 087' WHERE service_id = '1466';""")

def downgrade():

    # Generated SQL commands for downgrade (rollback)
    op.execute("""UPDATE service SET service_code = 'Other - 87' WHERE service_id = '1466';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1293';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1292';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1291';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1290';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1288';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1285';""")
    op.execute("""UPDATE service SET prefix = 'a' WHERE service_id = '1279';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
 ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
 How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
 What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '1125';""")
    op.execute("""UPDATE service SET online_link = 'https:\www2.gov.bc.ca/getvaccinated.html' WHERE service_id = '984';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
 Jurisdiction and Roll Number of Property 
 Your Property Address
 Valid Photo ID (BC Driverâs Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
 Your Social Insurance Number 
 Municipal Property Taxation Notice (helpful not required)

Please Note:  SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '916';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
	Valid Photo ID (BC Driverâs Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
	Your Declaration Code and Letter ID (found on your Declaration Letter)
	Your Social Insurance Number 
	Your property address
	The Representative of Deceased Owner will also need the Will, Grant of Administration or Grant of Probate.  

ONLINE OPTION:   https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax 

 



' WHERE service_id = '572';""")
    op.execute("""UPDATE service SET prefix = 'b' WHERE service_id = '554';""")
    op.execute("""UPDATE service SET online_link = 'https://justice.gov.bc.ca/cannabislicensing/policy-document/worker-qualification-home ' WHERE service_id = '507';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
 ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp 
 Getting your Learners Licence: https://www.icbc.com/driver-licensing/new-drivers/Pages/Get-your-L.aspx 
 Getting your Commercial Licence: https://www.icbc.com/driver-licensing/types-licences/Pages/Get-your-commercial-driver-licence.aspx 
 What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '313';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
 ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
 How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
 What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '304';""")
    op.execute("""UPDATE service SET email_paragraph = '' WHERE service_id = '169';""")
    op.execute("""UPDATE service SET email_paragraph = '' WHERE service_id = '166';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
 Jurisdiction and Roll Number of Property 
 Your Property Address
 Valid Photo ID (BC Driverâs Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
 Your Social Insurance Number 
 Property Taxation Notice (helpful not required)

Please Note: SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '94';""")