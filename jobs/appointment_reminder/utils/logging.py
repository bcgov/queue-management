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
"""Centralized setup of logging for the service."""
import logging.config
import sys
from os import path


def setup_logging(conf):
    """Create the services logger.

    TODO should be reworked to load in the proper loggers and remove others
    """
    # log_file_path = path.join(path.abspath(path.dirname(__file__)), conf)

    if conf and path.isfile(conf):
        logging.config.fileConfig(conf)
        print('Configure logging, from conf:{}'.format(conf), file=sys.stdout)
    else:
        print('Unable to configure logging, attempted conf:{}'.format(conf), file=sys.stderr)
