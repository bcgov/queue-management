"""empty message

Revision ID: 223526cbd142
Revises: b0f5b7b6acf7
Create Date: 2019-01-18 10:12:38.754879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '223526cbd142'
down_revision = 'b0f5b7b6acf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exam', sa.Column('offsite_location', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exam', 'offsite_location')
    # ### end Alembic commands ###
