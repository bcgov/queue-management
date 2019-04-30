"""empty message

Revision ID: 6a7246416d91
Revises: 68dc9380b8c0
Create Date: 2019-04-08 01:48:42.349845

"""
from alembic import op
import sqlalchemy as sa
from qsystem import db
from app.models.theq import Office, CSR, Counter

# revision identifiers, used by Alembic.
revision = '6a7246416d91'
down_revision = '68dc9380b8c0'
branch_labels = None
depends_on = None


def upgrade():

    quick_trans_counter = Counter.query.filter_by(counter_name="Quick Trans").first()
    regular_counter = Counter.query.filter_by(counter_name="Counter").first()

    print('createing counters...')
    if not quick_trans_counter:
        quick_trans_counter = Counter(
            counter_name='Quick Trans'
        )
        regular_counter = Counter(
            counter_name='Counter'
        )

        db.session.add(quick_trans_counter)
        db.session.add(regular_counter)
        db.session.commit()
    print("adding counters to offices...")

    for office in Office.query.all():
        if regular_counter not in office.counters:
            office.counters.append(regular_counter)
        if quick_trans_counter not in office.counters:
            office.counters.append(quick_trans_counter)
        db.session.add(office)

    db.session.commit()

    print("adding counters to csrs...")
    for csr in CSR.query.all():
        if csr.qt_xn_csr_ind:
            csr.counter = quick_trans_counter
        else:
            csr.counter = regular_counter
        db.session.add(csr)
    
    db.session.commit()


def downgrade():
    # Data-only migration, so we won't bother with this, and make the upgrade idempotent instead.
    pass
