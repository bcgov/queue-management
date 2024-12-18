"""sbcq253_dev_prod_push_examtype

Revision ID: f364ea9bfb7e
Revises: af7da4ef41da
Create Date: 2024-10-04 12:53:06.352929

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'f364ea9bfb7e'
down_revision = 'af7da4ef41da'
branch_labels = None
depends_on = None


def upgrade():

    # Generated SQL commands for upgrade
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide ** DO NOT USE **', pesticide_exam_ind = '1', deleted = '2021-05-17 17:11:00' WHERE exam_type_id = '70';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide 1.5 Hour  ** DO NOT USE **', pesticide_exam_ind = '1', number_of_minutes = '30', deleted = '2021-05-17 17:12:00' WHERE exam_type_id = '72';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide 1 Hour ** DO NOT USE **', number_of_hours = '1', pesticide_exam_ind = '1', deleted = '2021-05-17 17:12:00' WHERE exam_type_id = '75';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide 4 Hour ** DO NOT USE **', pesticide_exam_ind = '1', deleted = '2021-05-17 17:12:00' WHERE exam_type_id = '77';""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('135', 'THW - 1 Hour exam ****Do Not Use****', 'beige', '1', 'Written', '0', '0', '0', '0', '2021-05-18 17:10:00');""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('136', 'THW - 2 Hour exam ****Do Not Use****', 'beige', '2', 'Written', '0', '0', '0', '0', '2021-05-18 17:10:00');""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('137', 'Veterinary 2 Hour', '#FFFFFF', '2', 'Paper', '0', '0', '0', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('170', 'Misc. Pesticide 1 hour', '#FFFFFF', '1', 'Paper', '0', '0', '0', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('171', 'Misc. Pesticide 3 Hour', '#FFFFFF', '3', 'Paper', '0', '0', '0', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('172', 'THW-Asbestos', '#FFFFFF', '1', 'Written', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('173', 'THW-Battery', '#FFFFFF', '1', 'Written', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('174', 'THW-Biomedical', '#FFFFFF', '1', 'Written', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('175', 'THW-General', '#FFFFFF', '2', 'Written', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('176', 'THW-Petroleum', '#FFFFFF', '1', 'Written', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('207', 'Agriculture-RodentManagement', '#FFFFFF', '3', 'Paper', '0', '0', '1', '0', NULL);""")
    op.execute("""INSERT INTO examtype (exam_type_id, exam_type_name, exam_color, number_of_hours, method_type, ita_ind, group_exam_ind, pesticide_exam_ind, number_of_minutes, deleted) VALUES ('208', 'THW-testing-Do not use this', '#FFFFFF', '1', 'Written', '0', '0', '1', '0', NULL);""")


def downgrade():

    # Generated SQL commands for downgrade (rollback)
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '208';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '207';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '176';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '175';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '174';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '173';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '172';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '171';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '170';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '137';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '136';""")
    op.execute("""DELETE FROM examtype WHERE exam_type_id = '135';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide 4 Hour - DO NOT USE', pesticide_exam_ind = '0', deleted = NULL WHERE exam_type_id = '77';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Misc. Pesticide 3 Hour', number_of_hours = '3', pesticide_exam_ind = '0', deleted = NULL WHERE exam_type_id = '75';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Misc. Pesticide 1 Hour', pesticide_exam_ind = '0', number_of_minutes = '0', deleted = NULL WHERE exam_type_id = '72';""")
    op.execute("""UPDATE examtype SET exam_type_name = 'Pesticide - DO NOT USE', pesticide_exam_ind = '0', deleted = NULL WHERE exam_type_id = '70';""")
