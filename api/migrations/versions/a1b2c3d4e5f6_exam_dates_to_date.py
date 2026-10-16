"""Convert exam expiry, received, and returned dates to calendar dates.

Revision ID: a1b2c3d4e5f6
Revises: 8b6c67545310
Create Date: 2026-10-16 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '8b6c67545310'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'exam',
        'expiry_date',
        existing_type=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using="(expiry_date AT TIME ZONE 'UTC')::date",
    )
    op.alter_column(
        'exam',
        'exam_received_date',
        existing_type=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using="(exam_received_date AT TIME ZONE 'UTC')::date",
    )
    op.alter_column(
        'exam',
        'exam_returned_date',
        existing_type=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using="(exam_returned_date AT TIME ZONE 'UTC')::date",
    )


def downgrade():
    op.alter_column(
        'exam',
        'exam_returned_date',
        existing_type=sa.Date(),
        type_=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="(exam_returned_date::timestamp AT TIME ZONE 'UTC')",
    )
    op.alter_column(
        'exam',
        'exam_received_date',
        existing_type=sa.Date(),
        type_=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="(exam_received_date::timestamp AT TIME ZONE 'UTC')",
    )
    op.alter_column(
        'exam',
        'expiry_date',
        existing_type=sa.Date(),
        type_=sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="(expiry_date::timestamp AT TIME ZONE 'UTC')",
    )
