'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''


from qsystem import db, application
import os
import tempfile
import unittest


class TheQTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_fd, application.config['DATABASE'] = tempfile.mkstemp()
        application.testing = True
        cls.app = application.test_client()

        with application.app_context():
            db.init_app(application)
            db.drop_all()
            db.create_all()

        cls.client = application.test_client()

    def test_health(self):
        with application.app_context():
            rv = self.client.get("/api/v1/healthz/")
            assert '200' in rv.status
            assert b'api is healthy' in rv.data

    def test_ready(self):
        with application.app_context():
            rv = self.client.get("/api/v1/readyz/")
            assert '200' in rv.status
            assert b'api is ready' in rv.data

    @classmethod
    def tearDownClass(cls):
        os.close(cls.db_fd)
        os.unlink(application.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
