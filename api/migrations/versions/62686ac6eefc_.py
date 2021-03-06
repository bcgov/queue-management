"""empty message

Revision ID: 62686ac6eefc
Revises: 664c765d1547
Create Date: 2021-02-17 20:41:14.110155

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = '62686ac6eefc'
down_revision = '664c765d1547'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('stat_flag', sa.Boolean(), nullable=True))
    op.add_column('booking', sa.Column('stat_flag', sa.Boolean(), nullable=True))
    op.execute("UPDATE appointment SET stat_flag = false")
    op.execute("UPDATE booking SET stat_flag = false")
    op.alter_column('appointment', 'stat_flag', nullable=False)
    op.alter_column('booking', 'stat_flag', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('booking', 'stat_flag')
    op.drop_column('appointment', 'stat_flag')
    # ### end Alembic commands ###
