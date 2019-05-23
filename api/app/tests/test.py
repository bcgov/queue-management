import json
import os
import tempfile
import unittest

from qsystem import db, application
from app.models import theq
from app.schemas.theq import ServiceReqSchema


class QSystemTestCase(unittest.TestCase):

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
            service_request_schema = ServiceReqSchema()

            json_data = {'service_id': 12, 'citizen_id': '', 'quantity': 3, 'channel_id': 2}
            
            service_request = service_request_schema.load(json_data).data

            # Confirm a marshmallow bug, returns a dict when invalid data passed in.
            assert type(service_request) is dict


    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(application.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
