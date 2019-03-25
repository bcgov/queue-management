"""empty message

Revision ID: 5403058507a5
Revises: 0e0a38cb41aa
Create Date: 2019-03-25 17:42:59.297496

"""
from alembic import op
import sqlalchemy as sa


revision = '5403058507a5'
down_revision = '0e0a38cb41aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('counter',
    sa.Column('counter_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('counter_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('counter_id')
    )
    op.create_table('office_counter',
    sa.Column('office_id', sa.Integer(), nullable=False),
    sa.Column('counter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['counter_id'], ['counter.counter_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('office_id', 'counter_id')
    )
    op.create_table('office_quick_list',
    sa.Column('office_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('office_id', 'service_id')
    )


def downgrade():
    op.drop_table('office_quick_list')
    op.drop_table('office_counter')
    op.drop_table('counter')
