"""add_off_id_and_deleted

Revision ID: 4ccc950a7aa2
Revises: 89294ac623e8
Create Date: 2020-06-30 15:05:50.840123

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '4ccc950a7aa2'
down_revision = '89294ac623e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeslot', sa.Column('deleted', sa.DateTime(), nullable=True))
    op.add_column('timeslot', sa.Column('office_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'timeslot', 'office', ['office_id'], ['office_id'])
    op.execute("update timeslot set office_id=office_timeslot.office_id from office_timeslot where timeslot.time_slot_id=office_timeslot.time_slot_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'timeslot', type_='foreignkey')
    op.drop_column('timeslot', 'office_id')
    op.drop_column('timeslot', 'deleted')
    # ### end Alembic commands ###
