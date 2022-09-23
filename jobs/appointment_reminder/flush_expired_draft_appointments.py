# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Update Payment Job.

This module is being invoked from a job and it cleans up the stale records
"""
from utils.logging import setup_logging

import os
import sys

from flask import Flask

import config


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Return a configured Flask App using the Factory method."""
    from qsystem import db

    app = Flask(__name__)

    app.config.from_object(config.CONFIGURATION[run_mode])
    app.logger.info(f'<<<< Starting Flush Expired Drafts Jobs >>>>')
    db.init_app(app)

    register_shellcontext(app)

    return app

def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'app': app
        }  # pragma: no cover

    app.shell_context_processor(shell_context)



def run():
    application = create_app()
    application.app_context().push()
    flush_drafts(application)

def flush_drafts(app):
    app.logger.debug('<<< Starting flush_drafts job')

    # get appointment query, for now just select *

    return 'todo'
    

if __name__ == "__main__":
    run()
