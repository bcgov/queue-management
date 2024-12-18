"""sbcq242_service_name

Revision ID: d56650c6d5b8
Revises: 516321784cb2
Create Date: 2024-10-09 17:23:57.165509

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'd56650c6d5b8'
down_revision = '516321784cb2'
branch_labels = None
depends_on = None


def upgrade():

    # Generated SQL commands for upgrade
    op.execute("""UPDATE service SET service_name = 'Evidence - Additional' WHERE service_id = '466';""")
    op.execute("""UPDATE service SET service_name = 'Other - Mobile' WHERE service_id = '487';""")
    op.execute("""UPDATE service SET service_name = 'Cannabis & Liquor Services' WHERE service_id = '519';""")
    op.execute("""UPDATE service SET service_name = 'Autism Funding' WHERE service_id = '522';""")
    op.execute("""UPDATE service SET service_name = 'COVID Office' WHERE service_id = '652';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler Calls' WHERE service_id = '654';""")
    op.execute("""UPDATE service SET service_name = 'ESB - Variance Paper Application' WHERE service_id = '724';""")
    op.execute("""UPDATE service SET service_name = 'ESB - CATs - Direct to online Variance App.' WHERE service_id = '725';""")
    op.execute("""UPDATE service SET service_name = 'ESB - Restricted - Variance Review' WHERE service_id = '726';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing' WHERE service_id = '727';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing' WHERE service_id = '728';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing' WHERE service_id = '729';""")
    op.execute("""UPDATE service SET service_name = 'Election BC - Bundling Ballots' WHERE service_id = '763';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist - BCP' WHERE service_id = '764';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist - BCP' WHERE service_id = '765';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist - BCP' WHERE service_id = '766';""")
    op.execute("""UPDATE service SET service_name = 'CCII - Complaints' WHERE service_id = '800';""")
    op.execute("""UPDATE service SET service_name = 'CCII - Compliments' WHERE service_id = '801';""")
    op.execute("""UPDATE service SET service_name = 'CCII - Suggestions' WHERE service_id = '802';""")
    op.execute("""UPDATE service SET service_name = 'THW - Exam' WHERE service_id = '869';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application - New' WHERE service_id = '874';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application - Renewal' WHERE service_id = '875';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence - Renewal' WHERE service_id = '877';""")
    op.execute("""UPDATE service SET service_name = 'Online Verification Tier 2' WHERE service_id = '878';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence - GVA Payment ' WHERE service_id = '912';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application - GVA Payment  ' WHERE service_id = '913';""")
    op.execute("""UPDATE service SET service_name = 'Muni HOG - Information' WHERE service_id = '917';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence - email App. ONLY' WHERE service_id = '1053';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application - email ONLY' WHERE service_id = '1054';""")
    op.execute("""UPDATE service SET service_name = 'Tech. Assistance - 7-7000' WHERE service_id = '1056';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine - Federal Vaccination Card' WHERE service_id = '1126';""")
    op.execute("""UPDATE service SET service_name = 'MTO - Assistance' WHERE service_id = '1239';""")
    op.execute("""UPDATE service SET service_name = 'CATe Pharmacy contact' WHERE service_id = '1278';""")
    op.execute("""UPDATE service SET service_name = 'BC REG Tier 2 - Corporations' WHERE service_id = '1394';""")
    op.execute("""UPDATE service SET service_name = 'BC REG Tier 2 - Corporations' WHERE service_id = '1395';""")
    op.execute("""UPDATE service SET service_name = 'THW/IPM Licence - SBC Internal' WHERE service_id = '1400';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine - Liaison/Program Specialist' WHERE service_id = '1433';""")
    op.execute("""UPDATE service SET service_name = 'ERA App Support' WHERE service_id = '1536';""")

def downgrade():

    # Generated SQL commands for downgrade (rollback)
    op.execute("""UPDATE service SET service_name = 'ERA Program Support' WHERE service_id = '1536';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine  Liaison/Program Specialist' WHERE service_id = '1433';""")
    op.execute("""UPDATE service SET service_name = 'THW/IPM Licence  SBC Internal' WHERE service_id = '1400';""")
    op.execute("""UPDATE service SET service_name = 'BC Reg Tier 2 - Corporations' WHERE service_id = '1395';""")
    op.execute("""UPDATE service SET service_name = 'BC Reg Tier 2 - Corporations' WHERE service_id = '1394';""")
    op.execute("""UPDATE service SET service_name = 'CATe Pharmacy contact ' WHERE service_id = '1278';""")
    op.execute("""UPDATE service SET service_name = 'MTO  Assistance' WHERE service_id = '1239';""")
    op.execute("""UPDATE service SET service_name = 'Vaccine  Federal Vaccination Card' WHERE service_id = '1126';""")
    op.execute("""UPDATE service SET service_name = 'Tech. Assistance  7-7000 ' WHERE service_id = '1056';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application  email ONLY ' WHERE service_id = '1054';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence  email App. ONLY ' WHERE service_id = '1053';""")
    op.execute("""UPDATE service SET service_name = 'Muni HOG - Information ' WHERE service_id = '917';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application  GVA Payment  ' WHERE service_id = '913';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence  GVA Payment  ' WHERE service_id = '912';""")
    op.execute("""UPDATE service SET service_name = 'Online Verification Tier 2 ' WHERE service_id = '878';""")
    op.execute("""UPDATE service SET service_name = 'THW Licence - Renewal ' WHERE service_id = '877';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application  Renewal ' WHERE service_id = '875';""")
    op.execute("""UPDATE service SET service_name = 'PEST Licence Application  New' WHERE service_id = '874';""")
    op.execute("""UPDATE service SET service_name = 'THW - Exam ' WHERE service_id = '869';""")
    op.execute("""UPDATE service SET service_name = 'CCII  Suggestions' WHERE service_id = '802';""")
    op.execute("""UPDATE service SET service_name = 'CCII  Compliments' WHERE service_id = '801';""")
    op.execute("""UPDATE service SET service_name = 'CCII  Complaints' WHERE service_id = '800';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist  BCP ' WHERE service_id = '766';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist  BCP ' WHERE service_id = '765';""")
    op.execute("""UPDATE service SET service_name = 'Liaison/Prog Specialist  BCP ' WHERE service_id = '764';""")
    op.execute("""UPDATE service SET service_name = 'Election BC  Bundling Ballots' WHERE service_id = '763';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing ' WHERE service_id = '729';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing ' WHERE service_id = '728';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler - Camunda Testing ' WHERE service_id = '727';""")
    op.execute("""UPDATE service SET service_name = 'ESB  Restricted - Variance Review' WHERE service_id = '726';""")
    op.execute("""UPDATE service SET service_name = 'ESB  CATs - Direct to online Variance App.' WHERE service_id = '725';""")
    op.execute("""UPDATE service SET service_name = 'ESB  Variance Paper Application' WHERE service_id = '724';""")
    op.execute("""UPDATE service SET service_name = 'COVID Traveler Calls ' WHERE service_id = '654';""")
    op.execute("""UPDATE service SET service_name = 'COVID Office ' WHERE service_id = '652';""")
    op.execute("""UPDATE service SET service_name = 'Autism Funding ' WHERE service_id = '522';""")
    op.execute("""UPDATE service SET service_name = 'Other  Cannabis & Liquor' WHERE service_id = '519';""")
    op.execute("""UPDATE service SET service_name = 'Other - Mobile ' WHERE service_id = '487';""")
    op.execute("""UPDATE service SET service_name = 'Evidence - Additional ' WHERE service_id = '466';""")