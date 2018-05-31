import json
import os
import tempfile
import unittest

from qsystem import db, application
from app.models import Note

class QSystemNoteTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, application.config['DATABASE'] = tempfile.mkstemp()
        application.testing = True
        self.app = application.test_client()

        with application.app_context():
            db.init_app(application)
            db.drop_all()
            db.create_all()

    def test_create_edit_delete_note(self):
        with application.app_context():
            #Ensure no notes exist
            notes = db.session.query(Note).all()
            assert len(notes) == 0

            #Now create a note
            note = Note(value="test")
            db.session.add(note)

            #Query to check that it was added
            notes = db.session.query(Note).all()
            assert len(notes) == 1

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(application.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
