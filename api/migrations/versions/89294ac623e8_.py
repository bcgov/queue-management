"""empty message

Revision ID: 89294ac623e8
Revises: 05301cda7812
Create Date: 2020-04-01 19:42:56.383186

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '89294ac623e8'
down_revision = '05301cda7812'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('exam', sa.Column('candidates_list', sa.JSON(), nullable=True))
    op.add_column('exam', sa.Column('is_pesticide', sa.Integer(), nullable=True, default=0))


def downgrade():
    op.drop_column('exam', 'candidates_list')
    op.drop_column('exam', 'is_pesticide')
