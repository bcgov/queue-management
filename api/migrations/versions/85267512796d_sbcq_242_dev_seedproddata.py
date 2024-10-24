"""sbcq_242_dev_seedproddata

Revision ID: 85267512796d
Revises: f364ea9bfb7e
Create Date: 2024-10-03 15:00:14.252151

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '85267512796d'
down_revision = 'f364ea9bfb7e'
branch_labels = None
depends_on = None


def upgrade():

    # Generated SQL commands for upgrade
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '67';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '70';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '76';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
 ¢ Jurisdiction and Roll Number of Property 
 ¢ Your Property Address
 ¢ Valid Photo ID (BC Driver  s Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
 ¢ Your Social Insurance Number 
 ¢ Property Taxation Notice (helpful not required)

Please Note: SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '94';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '136';""")
    op.execute("""UPDATE service SET service_desc = 'RTB    Assisting citizens with online applications at CATs.  Back office duties such as management of Abandoned files.  Other misc. services' WHERE service_id = '142';""")
    op.execute("""UPDATE service SET service_desc = 'SkilledTradesBC   Invigilation - one-off;  Pre/During/Post - All work involved from receiving the exam, to mailing the completed exam and materials to SkilledTradesBC and BC Mail. ' WHERE service_id = '160';""")
    op.execute("""UPDATE service SET service_desc = 'PEST Invigilation - one-off;  Pre/During/Post - All work involved from scheduling the candidate, to uploading the completed materials.   ' WHERE service_id = '175';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '187';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '193';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '199';""")
    op.execute("""UPDATE service SET service_desc = 'Providing Information for misc. programs, applications such as gaming, photocopies, faxes, misc. forms, Front Counter BC, Human Rights Tribunal, Public Trustee, Legal Aid, bereavement checklist, foreign pension, Safer, HAFI, BC Housing, Seafood Licencing etc.     Payments such as ministry collections and student loans (e.g., Service Code 1278/Revenue Services of BC (RSBC), MCFD SC1459, , Mineral Tax., Mineral Inspection, , Bridge Toll etc.' WHERE service_id = '220';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '235';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '241';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '244';""")
    op.execute("""UPDATE service SET service_desc = 'Batching ', deleted = NULL WHERE service_id = '247';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '250';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '253';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '256';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '259';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '262';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '265';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '268';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '271';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '274';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '280';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '286';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '289';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
 ¢ ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
 ¢ How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
 ¢ What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '304';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
 ¢ ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp 
 ¢ Getting your Learners Licence: https://www.icbc.com/driver-licensing/new-drivers/Pages/Get-your-L.aspx 
 ¢ Getting your Commercial Licence: https://www.icbc.com/driver-licensing/types-licences/Pages/Get-your-commercial-driver-licence.aspx 
 ¢ What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '313';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '328';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '331';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '472';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '496';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '499';""")
    op.execute("""UPDATE service SET deleted = NULL, online_link = 'https://justice.gov.bc.ca/cannabislicensing/policy-document/worker-qualification-home ' WHERE service_id = '507';""")
    op.execute("""UPDATE service SET service_desc = 'SC 1664    Completing a Worker Attestation, Taking $100 payment, Witnessing signature, coping ID, scanning to LCRB etc.' WHERE service_id = '510';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '516';""")
    op.execute("""UPDATE service SET service_name = 'Other    Cannabis & Liquor' WHERE service_id = '519';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '525';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '527';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '536';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '539';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '542';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '545';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '551';""")
    op.execute("""UPDATE service SET deleted = NULL, prefix = 'b' WHERE service_id = '554';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '557';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '560';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '563';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '569';""")
    op.execute("""UPDATE service SET deleted = NULL, email_paragraph = 'Know what to bring to your appointment
 ¢	Valid Photo ID (BC Driver  s Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
 ¢	Your Declaration Code and Letter ID (found on your Declaration Letter)
 ¢	Your Social Insurance Number 
 ¢	Your property address
 ¢	The Representative of Deceased Owner will also need the Will, Grant of Administration or Grant of Probate.  

ONLINE OPTION:   https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax 

 



' WHERE service_id = '572';""")
    op.execute("""UPDATE service SET service_desc = 'SC800, Speculation Tax, SVT, taking a vacancy SVT   payment.' WHERE service_id = '575';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '577';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '583';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '586';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '589';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '592';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '598';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '603';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '612';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '613';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '614';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '615';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '616';""")
    op.execute("""UPDATE service SET service_desc = 'RTB    Providing Information for general program and application processes, RTB contact info, printing and providing forms' WHERE service_id = '617';""")
    op.execute("""UPDATE service SET service_desc = 'F&W - Royalty Payments, Any BACK OFFICE work issuing licences/creating FWIDs for Guides  (i.e.  bulk drop off  licence requests).  Track FRONT COUNTER  services as Hunting    Non-Resident' WHERE service_id = '619';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '691';""")
    op.execute("""UPDATE service SET service_name = 'ESB    Variance Paper Application' WHERE service_id = '724';""")
    op.execute("""UPDATE service SET service_name = 'ESB    CATs - Direct to online Variance App.' WHERE service_id = '725';""")
    op.execute("""UPDATE service SET service_name = 'ESB    Restricted - Variance   Review', service_desc = 'Back office duty for specifically assigned SBC staff only - Employment Standards Branch     ' WHERE service_id = '726';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '730';""")
    op.execute("""UPDATE service SET service_name = 'Election BC    Bundling Ballots', service_desc = 'Preparing Ballot Bundles and mailing to Elections BC (Back office duty).  VERY IMPORTANT: Adjust the transaction  s "Quantity" number to match the number of   Bundles   being mailed.   ' WHERE service_id = '763';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist    BCP ' WHERE service_id = '764';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist    BCP ' WHERE service_id = '765';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist    BCP ' WHERE service_id = '766';""")
    op.execute("""UPDATE service SET service_desc = 'Room booking, setup, and management of room bookings for Ministries etc.   ' WHERE service_id = '798';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '799';""")
    op.execute("""UPDATE service SET service_name = 'CCII    Complaints' WHERE service_id = '800';""")
    op.execute("""UPDATE service SET service_name = 'CCII    Compliments' WHERE service_id = '801';""")
    op.execute("""UPDATE service SET service_name = 'CCII    Suggestions' WHERE service_id = '802';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '803';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '834';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '835';""")
    op.execute("""UPDATE service SET service_desc = 'All Contact Tracing Calls    TRACK EACH CALL SEPARATELY' WHERE service_id = '836';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste exam invigilation    Includes All Pre-Preparation, During, and Post duties performed for Onsite One-Off Exam Invigilation.   i.e.   from scheduling in The Q to submitting completed exam.', external_service_name = 'Transportation of Hazardous Waste Exams   to order phone 1-866-205-2102' WHERE service_id = '869';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation    Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '870';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation    Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '871';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation    Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '872';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application    New', service_desc = 'Pesticide Licence - New application - Providing information, reviewing application for completeness, accepting payment (SC 0431), submitting application on the citizens   behalf, returning original etc.      ' WHERE service_id = '874';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application    Renewal                                                 ', service_desc = 'Pesticide Licence - Renewal application - Providing information, reviewing application for completeness, accepting payment (SC 0432), submitting application on the citizens   behalf, returning original etc', external_service_name = 'Pesticide Licence Application    Renewal                    ' WHERE service_id = '875';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste licence - New application:   Providing information, reviewing application for completeness, accepting payment (SC 1539), submitting application on citizens   behalf, returning original etc. ' WHERE service_id = '876';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste licence - Renewal application:   Providing information, reviewing application for completeness, accepting payment (SC 1540) submitting application on the citizens   behalf, returning original etc.' WHERE service_id = '877';""")
    op.execute("""UPDATE service SET service_desc = 'Speculation Tax, SVT    Providing General Information ' WHERE service_id = '911';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence    GVA Payment                    ', service_desc = 'FSSS office taking a phone Payment for GVA - Receive citizen contact information from GVA, phone citizen from PCI compliant phone, process payment for New (SC1539) or Renewal (SC 1540) licence in eGarms, scan/email copy of receipt to GVA.  ' WHERE service_id = '912';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application    GVA Payment        ', service_desc = 'FSSS office taking a phone Payment for GVA -     Receive citizen contact information from GVA, phone citizen from PCI compliant phone, process payment for New (SC 0431) or Renewal (SC 0432) licence in eGarms, scan/email copy of receipt to GVA.' WHERE service_id = '913';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '914';""")
    op.execute("""UPDATE service SET service_desc = 'Employment Standards Branch (ESB) Tier 2 -   Providing team support/answering questions, developing training/reference materials, provide training, Quality Assurance etc.' WHERE service_id = '915';""")
    op.execute("""UPDATE service SET service_desc = 'Centralized Municipal Home Owner Grant    Process HOG in Gentax on behalf of home owner', email_paragraph = 'Know what to bring to your appointment
 ¢ Jurisdiction and Roll Number of Property 
 ¢ Your Property Address
 ¢ Valid Photo ID (BC Driver  s Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
 ¢ Your Social Insurance Number 
 ¢ Municipal Property Taxation Notice (helpful not required)

Please Note:  SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '916';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '949';""")
    op.execute("""UPDATE service SET online_link = 'https:\\www2.gov.bc.ca/getvaccinated.html' WHERE service_id = '984';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1017';""")
    op.execute("""UPDATE service SET service_desc = 'IMMS    Responding to an Ad Hoc/Misc. enquiry in the vaccination booking Call Back queue' WHERE service_id = '1050';""")
    op.execute("""UPDATE service SET deleted = NULL, external_service_name = 'ICBC services not available here; find your closest driver licensing office in Online Options  ', online_link = 'https://www.icbc.com/locators/Pages/default.aspx  ' WHERE service_id = '1051';""")
    op.execute("""UPDATE service SET service_desc = 'CPG - Community Gaming Grant Program 2021    Provide general application or contact information, scan and email documentation to citizen in support of their application, direct citizen to CATs if applying in the office. ' WHERE service_id = '1052';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence    email App. ONLY ', service_desc = 'Transportation of Hazardous Waste licence    New AND Renewal application received by email:   Reviewing application for completeness and submitting on citizens   behalf.   IMPORTANT:   Track phone payment using   THW/PEST    email app. Payment   service type.' WHERE service_id = '1053';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application    email ONLY ', service_desc = 'Pesticide Licence    New AND Renewal application received by email - Reviewing application for completeness and submitting on the citizens   behalf. IMPORTANT: Track phone payment using   THW/PEST    email app. Payment   service type.' WHERE service_id = '1054';""")
    op.execute("""UPDATE service SET service_desc = 'For offices that have a CSR(s), triage the line up to determine reason for visit, to advise of wait times, redirect etc.   PPE required. ' WHERE service_id = '1055';""")
    op.execute("""UPDATE service SET service_name = 'Tech. Assistance    7-7000 ', service_desc = 'When CSR is getting Personal or Office related PC/Network technical assistance from 250-387-7000; either by phone or when submitting an online request.   ' WHERE service_id = '1056';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1057';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1092';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
 ¢ ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
 ¢ How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
 ¢ What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '1125';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine    Federal Vaccination Card' WHERE service_id = '1126';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1127';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1160';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1162';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1228';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1229';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1230';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1231';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1232';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1234';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1235';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1236';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1237';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1238';""")
    op.execute("""UPDATE service SET service_name = 'MTO    Assistance' WHERE service_id = '1239';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1241';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1242';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1243';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1244';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1277';""")
    op.execute("""UPDATE service SET deleted = NULL, prefix = 'a' WHERE service_id = '1279';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1281';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1283';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1284';""")
    op.execute("""UPDATE service SET deleted = NULL, prefix = 'a' WHERE service_id = '1285';""")
    op.execute("""UPDATE service SET deleted = NULL, prefix = 'a' WHERE service_id = '1292';""")
    op.execute("""UPDATE service SET deleted = NULL, prefix = 'a' WHERE service_id = '1293';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1326';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1327';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1328';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1329';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1360';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1393';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1396';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1397';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1398';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1399';""")
    op.execute("""UPDATE service SET service_name = 'THW/IPM Licence    SBC Internal' WHERE service_id = '1400';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine    Liaison/Program Specialist' WHERE service_id = '1433';""")
    op.execute("""UPDATE service SET service_desc = 'Used by MSC SCSR  s to review Federal and Provincial benefit programs through the online benefit finder tool' WHERE service_id = '1466';""")
    op.execute("""UPDATE service SET deleted = NULL WHERE service_id = '1499';""")


def downgrade():

    # Generated SQL commands for downgrade (rollback)
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1499';""")
    op.execute("""UPDATE service SET service_desc = 'Used by MSC SCSR’s to review Federal and Provincial benefit programs through the online benefit finder tool' WHERE service_id = '1466';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine – Liaison/Program Specialist' WHERE service_id = '1433';""")
    op.execute("""UPDATE service SET service_name = 'THW/IPM Licence – SBC Internal' WHERE service_id = '1400';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1399';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1398';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1397';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1396';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1393';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1360';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1329';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1328';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1327';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1326';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', prefix = 'A' WHERE service_id = '1293';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', prefix = 'A' WHERE service_id = '1292';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', prefix = 'A' WHERE service_id = '1285';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1284';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1283';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1281';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', prefix = 'A' WHERE service_id = '1279';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1277';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1244';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1243';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1242';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1241';""")
    op.execute("""UPDATE service SET service_name = 'MTO – Assistance' WHERE service_id = '1239';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1238';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1237';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1236';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1235';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1234';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1232';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1231';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1230';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1229';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1228';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1162';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1160';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1127';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine – Federal Vaccination Card' WHERE service_id = '1126';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
• ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
• How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
• What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '1125';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1092';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1057';""")
    op.execute("""UPDATE service SET service_name = 'Tech. Assistance – 7-7000 ', service_desc = 'When CSR is getting Personal or Office related PC/Network technical assistance from 250-387-7000; either by phone or when submitting an online request.  ' WHERE service_id = '1056';""")
    op.execute("""UPDATE service SET service_desc = 'For offices that have a CSR(s), triage the line up to determine reason for visit, to advise of wait times, redirect etc.  PPE required. ' WHERE service_id = '1055';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application – email ONLY ', service_desc = 'Pesticide Licence – New AND Renewal application received by email - Reviewing application for completeness and submitting on the citizens’ behalf. IMPORTANT: Track phone payment using “THW/PEST – email app. Payment” service type.' WHERE service_id = '1054';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence – email App. ONLY ', service_desc = 'Transportation of Hazardous Waste licence – New AND Renewal application received by email:  Reviewing application for completeness and submitting on citizens’ behalf.  IMPORTANT:  Track phone payment using “THW/PEST – email app. Payment” service type.' WHERE service_id = '1053';""")
    op.execute("""UPDATE service SET service_desc = 'CPG - Community Gaming Grant Program 2021 – Provide general application or contact information, scan and email documentation to citizen in support of their application, direct citizen to CATs if applying in the office. ' WHERE service_id = '1052';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', external_service_name = 'ICBC services not available here; find your closest driver licensing office in Online Options', online_link = 'https://www.icbc.com/locators/Pages/default.aspx' WHERE service_id = '1051';""")
    op.execute("""UPDATE service SET service_desc = 'IMMS – Responding to an Ad Hoc/Misc. enquiry in the vaccination booking Call Back queue' WHERE service_id = '1050';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1017';""")
    op.execute("""UPDATE service SET online_link = 'https:\www2.gov.bc.ca/getvaccinated.html' WHERE service_id = '984';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '949';""")
    op.execute("""UPDATE service SET service_desc = 'Centralized Municipal Home Owner Grant – Process HOG in Gentax on behalf of home owner', email_paragraph = 'Know what to bring to your appointment
• Jurisdiction and Roll Number of Property 
• Your Property Address
• Valid Photo ID (BC Driver’s Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
• Your Social Insurance Number 
• Municipal Property Taxation Notice (helpful not required)

Please Note:  SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '916';""")
    op.execute("""UPDATE service SET service_desc = 'Employment Standards Branch (ESB) Tier 2 -  Providing team support/answering questions, developing training/reference materials, provide training, Quality Assurance etc.' WHERE service_id = '915';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '914';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application – GVA Payment     ', service_desc = 'FSSS office taking a phone Payment for GVA -   Receive citizen contact information from GVA, phone citizen from PCI compliant phone, process payment for New (SC 0431) or Renewal (SC 0432) licence in eGarms, scan/email copy of receipt to GVA.' WHERE service_id = '913';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence – GVA Payment                  ', service_desc = 'FSSS office taking a phone Payment for GVA - Receive citizen contact information from GVA, phone citizen from PCI compliant phone, process payment for New (SC1539) or Renewal (SC 1540) licence in eGarms, scan/email copy of receipt to GVA.         ' WHERE service_id = '912';""")
    op.execute("""UPDATE service SET service_desc = 'Speculation Tax, SVT – Providing General Information ' WHERE service_id = '911';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste licence - Renewal application:  Providing information, reviewing application for completeness, accepting payment (SC 1540) submitting application on the citizens’ behalf, returning original etc.' WHERE service_id = '877';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste licence - New application:  Providing information, reviewing application for completeness, accepting payment (SC 1539), submitting application on citizens’ behalf, returning original etc. ' WHERE service_id = '876';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application – Renewal                         ', service_desc = 'Pesticide Licence - Renewal application - Providing information, reviewing application for completeness, accepting payment (SC 0432), submitting application on the citizens’ behalf, returning original etc', external_service_name = 'Pesticide Licence Application – Renewal                    ' WHERE service_id = '875';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application – New', service_desc = 'Pesticide Licence - New application - Providing information, reviewing application for completeness, accepting payment (SC 0431), submitting application on the citizens’ behalf, returning original etc.           ' WHERE service_id = '874';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation – Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '872';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation – Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '871';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste group exam invigilation – Includes receiving and checking exam materials, pre-preparation of materials for Invigilator (or SBC Staff), post preparation of completed exams and submission.' WHERE service_id = '870';""")
    op.execute("""UPDATE service SET service_desc = 'Transportation of Hazardous Waste exam invigilation – Includes All Pre-Preparation, During, and Post duties performed for Onsite One-Off Exam Invigilation.  i.e.  from scheduling in The Q to submitting completed exam.', external_service_name = 'Transportation of Hazardous Waste Exams –to order phone 1-866-205-2102' WHERE service_id = '869';""")
    op.execute("""UPDATE service SET service_desc = 'All Contact Tracing Calls – TRACK EACH CALL SEPARATELY' WHERE service_id = '836';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '835';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '834';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '803';""")
    op.execute("""UPDATE service SET service_name = 'CCII – Suggestions' WHERE service_id = '802';""")
    op.execute("""UPDATE service SET service_name = 'CCII – Compliments' WHERE service_id = '801';""")
    op.execute("""UPDATE service SET service_name = 'CCII – Complaints' WHERE service_id = '800';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '799';""")
    op.execute("""UPDATE service SET service_desc = 'Room booking, setup, and management of room bookings for Ministries etc.  ' WHERE service_id = '798';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist – BCP ' WHERE service_id = '766';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist – BCP ' WHERE service_id = '765';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist – BCP ' WHERE service_id = '764';""")
    op.execute("""UPDATE service SET service_name = 'Election BC – Bundling Ballots', service_desc = 'Preparing Ballot Bundles and mailing to Elections BC (Back office duty).  VERY IMPORTANT: Adjust the transaction’s "Quantity" number to match the number of “Bundles” being mailed.   ' WHERE service_id = '763';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '730';""")
    op.execute("""UPDATE service SET service_name = 'ESB – Restricted - Variance  Review', service_desc = 'Back office duty for specifically assigned SBC staff only - Employment Standards Branch   ' WHERE service_id = '726';""")
    op.execute("""UPDATE service SET service_name = 'ESB – CATs - Direct to online Variance App.' WHERE service_id = '725';""")
    op.execute("""UPDATE service SET service_name = 'ESB – Variance Paper Application' WHERE service_id = '724';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '691';""")
    op.execute("""UPDATE service SET service_desc = 'F&W - Royalty Payments, Any BACK OFFICE work issuing licences/creating FWIDs for Guides  (i.e.  bulk drop off  licence requests).  Track FRONT COUNTER  services as Hunting – Non-Resident' WHERE service_id = '619';""")
    op.execute("""UPDATE service SET service_desc = 'RTB – Providing Information for general program and application processes, RTB contact info, printing and providing forms' WHERE service_id = '617';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '616';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '615';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '614';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '613';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '612';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '603';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '598';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '592';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '589';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '586';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '583';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '577';""")
    op.execute("""UPDATE service SET service_desc = 'SC800, Speculation Tax, SVT, taking a vacancy SVT  payment.' WHERE service_id = '575';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', email_paragraph = '' WHERE service_id = '572';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '569';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '563';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '560';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '557';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', prefix = 'B' WHERE service_id = '554';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '551';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '545';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '542';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '539';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '536';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '527';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '525';""")
    op.execute("""UPDATE service SET service_name = 'Other – Cannabis & Liquor' WHERE service_id = '519';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '516';""")
    op.execute("""UPDATE service SET service_desc = 'SC 1664 – Completing a Worker Attestation, Taking $100 payment, Witnessing signature, coping ID, scanning to LCRB etc.' WHERE service_id = '510';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00', online_link = 'https://justice.gov.bc.ca/cannabislicensing/policy-document/worker-qualification-home' WHERE service_id = '507';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '499';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '496';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '472';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '331';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '328';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
• ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp 
• Getting your Learners Licence: https://www.icbc.com/driver-licensing/new-drivers/Pages/Get-your-L.aspx 
• Getting your Commercial Licence: https://www.icbc.com/driver-licensing/types-licences/Pages/Get-your-commercial-driver-licence.aspx 
• What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '313';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment:
• ID Requirements: http://apps.icbc.com/licensing/id_wizard/page1.asp  
• How to renew your Licence or ID: https://www.icbc.com/driver-licensing/getting-licensed/Pages/Renew-your-licence-or-ID.aspx  
• What are the costs: https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Fees.aspx  ' WHERE service_id = '304';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '289';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '286';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '280';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '274';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '271';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '268';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '265';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '262';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '259';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '256';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '253';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '250';""")
    op.execute("""UPDATE service SET service_desc = 'Batching', deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '247';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '244';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '241';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '235';""")
    op.execute("""UPDATE service SET service_desc = 'Providing Information for misc. programs, applications such as gaming, photocopies, faxes, misc. forms, Front Counter BC, Human Rights Tribunal, Public Trustee, Legal Aid, bereavement checklist, foreign pension, Safer, HAFI, BC Housing, Seafood Licencing etc.   Payments such as ministry collections and student loans (e.g., Service Code 1278/Revenue Services of BC (RSBC), MCFD SC1459, , Mineral Tax., Mineral Inspection, , Bridge Toll etc.' WHERE service_id = '220';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '199';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '193';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '187';""")
    op.execute("""UPDATE service SET service_desc = 'PEST Invigilation - one-off; Pre/During/Post - All work involved from scheduling the candidate, to uploading the completed materials.  ' WHERE service_id = '175';""")
    op.execute("""UPDATE service SET service_desc = 'SkilledTradesBC  Invigilation - one-off;  Pre/During/Post - All work involved from receiving the exam, to mailing the completed exam and materials to SkilledTradesBC and BC Mail. ' WHERE service_id = '160';""")
    op.execute("""UPDATE service SET service_desc = 'RTB – Assisting citizens with online applications at CATs.  Back office duties such as management of Abandoned files.  Other misc. services' WHERE service_id = '142';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '136';""")
    op.execute("""UPDATE service SET email_paragraph = 'Know what to bring to your appointment
• Jurisdiction and Roll Number of Property 
• Your Property Address
• Valid Photo ID (BC Driver’s Licence, BC Identification Card, BC services Card, Citizenship Card or Permanent Resident Card, Passport)
• Your Social Insurance Number 
• Property Taxation Notice (helpful not required)

Please Note: SERVICE BC DOES NOT ACCEPT PAYMENTS FOR MUNICIPAL PROPERTIES.

REMINDER YOU MAY CLAIM THE HOMEOWNER GRANT ONLINE: https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant/apply  ' WHERE service_id = '94';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '76';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '70';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '67';""")
    op.execute("""UPDATE service SET deleted = '2024-08-26 01:00:00+00:00' WHERE service_id = '1';""")
