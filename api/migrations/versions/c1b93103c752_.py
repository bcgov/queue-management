"""empty message

Revision ID: c1b93103c752
Revises: 
Create Date: 2019-05-23 15:29:33.842103

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc

# revision identifiers, used by Alembic.
revision = 'c1b93103c752'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'channel',
        sa.Column('channel_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('channel_name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('channel_id')
    )
    op.create_table(
        'citizenstate',
        sa.Column('cs_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cs_state_name', sa.String(length=100), nullable=False),
        sa.Column('cs_state_desc', sa.String(length=1000), nullable=False),
        sa.PrimaryKeyConstraint('cs_id')
    )
    op.create_table(
        'counter',
        sa.Column('counter_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('counter_name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('counter_id')
    )
    op.create_table(
        'csrstate',
        sa.Column('csr_state_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('csr_state_name', sa.String(length=50), nullable=False),
        sa.Column('csr_state_desc', sa.String(length=1000), nullable=False),
        sa.PrimaryKeyConstraint('csr_state_id')
    )
    op.create_table(
        'examtype',
        sa.Column('exam_type_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('exam_type_name', sa.String(length=50), nullable=False),
        sa.Column('exam_color', sa.String(length=10), nullable=False),
        sa.Column('number_of_hours', sa.Integer(), nullable=False),
        sa.Column('number_of_minutes', sa.Integer(), nullable=True),
        sa.Column('method_type', sa.String(length=10), nullable=False),
        sa.Column('ita_ind', sa.Integer(), nullable=False),
        sa.Column('group_exam_ind', sa.Integer(), nullable=False),
        sa.Column('pesticide_exam_ind', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('exam_type_id')
    )
    op.create_table(
        'metadata',
        sa.Column('metadata_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('meta_text', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('metadata_id')
    )
    op.create_table(
        'periodstate',
        sa.Column('ps_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ps_name', sa.String(length=100), nullable=False),
        sa.Column('ps_desc', sa.String(length=1000), nullable=False),
        sa.Column('ps_number', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('ps_id')
    )
    op.create_table(
        'permission',
        sa.Column('permission_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('permission_code', sa.String(length=100), nullable=False),
        sa.Column('permission_desc', sa.String(length=1000), nullable=False),
        sa.PrimaryKeyConstraint('permission_id')
    )
    op.create_table(
        'role',
        sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('role_code', sa.String(length=100), nullable=True),
        sa.Column('role_desc', sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table(
        'service',
        sa.Column('service_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('service_code', sa.String(length=50), nullable=False),
        sa.Column('service_name', sa.String(length=500), nullable=False),
        sa.Column('service_desc', sa.String(length=2000), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('prefix', sa.String(length=10), nullable=False),
        sa.Column('display_dashboard_ind', sa.Integer(), nullable=False),
        sa.Column('actual_service_ind', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['service.service_id'], ),
        sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table(
        'smartboard',
        sa.Column('sb_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sb_type', sa.String(length=45), nullable=False),
        sa.PrimaryKeyConstraint('sb_id')
    )
    op.create_table(
        'srstate',
        sa.Column('sr_state_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sr_code', sa.String(length=100), nullable=False),
        sa.Column('sr_state_desc', sa.String(length=1000), nullable=False),
        sa.PrimaryKeyConstraint('sr_state_id')
    )
    op.create_table(
        'timezone',
        sa.Column('timezone_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('timezone_name', sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint('timezone_id')
    )
    op.create_table(
        'office',
        sa.Column('office_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('office_name', sa.String(length=100), nullable=True),
        sa.Column('office_number', sa.Integer(), nullable=True),
        sa.Column('sb_id', sa.Integer(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('exams_enabled_ind', sa.Integer(), nullable=False),
        sa.Column('appointments_enabled_ind', sa.Integer(), nullable=False),
        sa.Column('timezone_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['sb_id'], ['smartboard.sb_id'], ),
        sa.ForeignKeyConstraint(['timezone_id'], ['timezone.timezone_id'], ),
        sa.PrimaryKeyConstraint('office_id')
    )
    op.create_table(
        'role_permission',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permission.permission_id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.create_table(
        'service_metadata',
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('metadata_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['metadata_id'], ['metadata.metadata_id'], ),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ),
        sa.PrimaryKeyConstraint('service_id', 'metadata_id')
    )
    op.create_table(
        'appointment',
        sa.Column('appointment_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
        sa.Column('end_time', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
        sa.Column('checked_in_time', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=True),
        sa.Column('comments', sa.String(length=255), nullable=True),
        sa.Column('citizen_name', sa.String(length=255), nullable=False),
        sa.Column('contact_information', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ),
        sa.PrimaryKeyConstraint('appointment_id')
    )
    op.create_table(
        'citizen',
        sa.Column('citizen_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('counter_id', sa.Integer(), nullable=True),
        sa.Column('ticket_number', sa.String(length=50), nullable=True),
        sa.Column('citizen_name', sa.String(length=150), nullable=True),
        sa.Column('citizen_comments', sa.String(length=1000), nullable=True),
        sa.Column('qt_xn_citizen_ind', sa.Integer(), nullable=False),
        sa.Column('cs_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('accurate_time_ind', sa.Integer(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['counter_id'], ['counter.counter_id'], ),
        sa.ForeignKeyConstraint(['cs_id'], ['citizenstate.cs_id'], ),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.PrimaryKeyConstraint('citizen_id')
    )
    op.create_table(
        'csr',
        sa.Column('csr_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=150), nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('counter_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('qt_xn_csr_ind', sa.Integer(), nullable=False),
        sa.Column('receptionist_ind', sa.Integer(), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('csr_state_id', sa.Integer(), nullable=False),
        sa.Column('ita_designate', sa.Integer(), nullable=False),
        sa.Column('pesticide_designate', sa.Integer(), nullable=False),
        sa.Column('finance_designate', sa.Integer(), nullable=False),
        sa.Column('liaison_designate', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['counter_id'], ['counter.counter_id'], ),
        sa.ForeignKeyConstraint(['csr_state_id'], ['csrstate.csr_state_id'], ),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
        sa.PrimaryKeyConstraint('csr_id'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'invigilator',
        sa.Column('invigilator_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('invigilator_name', sa.String(length=50), nullable=False),
        sa.Column('invigilator_notes', sa.String(length=400), nullable=True),
        sa.Column('contact_phone', sa.String(length=15), nullable=True),
        sa.Column('contact_email', sa.String(length=50), nullable=True),
        sa.Column('contract_number', sa.String(length=50), nullable=False),
        sa.Column('contract_expiry_date', sa.String(length=50), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.PrimaryKeyConstraint('invigilator_id')
    )
    op.create_table(
        'office_back_office_list',
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('office_id', 'service_id')
    )
    op.create_table(
        'office_counter',
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('counter_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['counter_id'], ['counter.counter_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('office_id', 'counter_id')
    )
    op.create_table(
        'office_quick_list',
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('office_id', 'service_id')
    )
    op.create_table(
        'office_service',
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('office_id', 'service_id')
    )
    op.create_table(
        'room',
        sa.Column('room_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('room_name', sa.String(length=50), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('color', sa.String(length=25), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.PrimaryKeyConstraint('room_id')
    )
    op.create_table(
        'booking',
        sa.Column('booking_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('invigilator_id', sa.Integer(), nullable=True),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
        sa.Column('end_time', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
        sa.Column('fees', sa.String(length=5), nullable=True),
        sa.Column('booking_name', sa.String(length=150), nullable=True),
        sa.Column('sbc_staff_invigilated', sa.Integer(), nullable=True),
        sa.Column('booking_contact_information', sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(['invigilator_id'], ['invigilator.invigilator_id'], ),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.ForeignKeyConstraint(['room_id'], ['room.room_id'], ),
        sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_table(
        'servicereq',
        sa.Column('sr_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('citizen_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('channel_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('sr_state_id', sa.Integer(), nullable=False),
        sa.Column('sr_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['channel_id'], ['channel.channel_id'], ),
        sa.ForeignKeyConstraint(['citizen_id'], ['citizen.citizen_id'], ),
        sa.ForeignKeyConstraint(['service_id'], ['service.service_id'], ),
        sa.ForeignKeyConstraint(['sr_state_id'], ['srstate.sr_state_id'], ),
        sa.PrimaryKeyConstraint('sr_id')
    )
    op.create_table(
        'exam',
        sa.Column('exam_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('booking_id', sa.Integer(), nullable=True),
        sa.Column('exam_type_id', sa.Integer(), nullable=False),
        sa.Column('office_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.String(length=25), nullable=True),
        sa.Column('exam_name', sa.String(length=50), nullable=False),
        sa.Column('examinee_name', sa.String(length=50), nullable=True),
        sa.Column('expiry_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.String(length=400), nullable=True),
        sa.Column('exam_received_date', sa.DateTime(), nullable=True),
        sa.Column('session_number', sa.Integer(), nullable=True),
        sa.Column('number_of_students', sa.Integer(), nullable=True),
        sa.Column('exam_method', sa.String(length=15), nullable=False),
        sa.Column('deleted_date', sa.String(length=50), nullable=True),
        sa.Column('exam_returned_date', sa.DateTime(), nullable=True),
        sa.Column('exam_returned_tracking_number', sa.String(length=255), nullable=True),
        sa.Column('exam_written_ind', sa.Integer(), nullable=False),
        sa.Column('offsite_location', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ondelete='set null'),
        sa.ForeignKeyConstraint(['exam_type_id'], ['examtype.exam_type_id'], ),
        sa.ForeignKeyConstraint(['office_id'], ['office.office_id'], ),
        sa.PrimaryKeyConstraint('exam_id')
    )
    op.create_table(
        'period',
        sa.Column('period_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sr_id', sa.Integer(), nullable=False),
        sa.Column('csr_id', sa.Integer(), nullable=False),
        sa.Column('reception_csr_ind', sa.Integer(), nullable=False),
        sa.Column('ps_id', sa.Integer(), nullable=False),
        sa.Column('time_start', sa.DateTime(), nullable=False),
        sa.Column('time_end', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['csr_id'], ['csr.csr_id'], ),
        sa.ForeignKeyConstraint(['ps_id'], ['periodstate.ps_id'], ),
        sa.ForeignKeyConstraint(['sr_id'], ['servicereq.sr_id'], ),
        sa.PrimaryKeyConstraint('period_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('period')
    op.drop_table('exam')
    op.drop_table('servicereq')
    op.drop_table('booking')
    op.drop_table('room')
    op.drop_table('office_service')
    op.drop_table('office_quick_list')
    op.drop_table('office_counter')
    op.drop_table('office_back_office_list')
    op.drop_table('invigilator')
    op.drop_table('csr')
    op.drop_table('citizen')
    op.drop_table('appointment')
    op.drop_table('service_metadata')
    op.drop_table('role_permission')
    op.drop_table('office')
    op.drop_table('timezone')
    op.drop_table('srstate')
    op.drop_table('smartboard')
    op.drop_table('service')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('periodstate')
    op.drop_table('metadata')
    op.drop_table('examtype')
    op.drop_table('csrstate')
    op.drop_table('counter')
    op.drop_table('citizenstate')
    op.drop_table('channel')
    # ### end Alembic commands ###
