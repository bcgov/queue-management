"""empty message

Revision ID: f54ebb773f4c
Revises: 0e0a38cb41aa
Create Date: 2019-03-24 21:12:25.078463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f54ebb773f4c'
down_revision = '0e0a38cb41aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('office_service', sa.Column(
        'quick_list_order', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('office_service', 'quick_list_order')
