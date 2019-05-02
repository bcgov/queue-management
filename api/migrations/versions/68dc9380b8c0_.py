"""empty message

Revision ID: 68dc9380b8c0
Revises: 5403058507a5
Create Date: 2019-03-25 18:27:48.779308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68dc9380b8c0'
down_revision = '5403058507a5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('csr', sa.Column('counter_id', sa.Integer(), nullable=True))
    op.add_column('citizen', sa.Column('counter_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'citizen', 'counter', ['counter_id'], ['counter_id'])
    op.create_foreign_key(None, 'csr', 'counter', ['counter_id'], ['counter_id'])
    

def downgrade():
    op.drop_constraint('csr_ibfk_4', 'csr', type_='foreignkey')
    op.drop_constraint('citizen_ibfk_3', 'citizen', type_='foreignkey')
    op.drop_column('csr', 'counter_id')
    op.drop_column('citizen', 'counter_id')
