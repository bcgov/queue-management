#!/bin/sh

# Copyright 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# Run the Cypress tests many times. Useful to run repeatedly and look for flaky
# tests. Exits when Cypress has an error.
#
# This is a very lazy MVP with no parameter checking, hard coded directory, etc.
#
# Example usage:
#    "cypress/runloop.sh" to run all tests repeatedly
#    "cypress/runloop.sh -s cypress/integration/image_snapshot/step1.spec.ts"
#        to run a single spec. Use it.only to run a single test within the spec.

cd /workspace/appointment-frontend

# Remove images from old runs so that test failures aren't confusing.
rm -rf cypress/snapshots/image_snapshot/*/__diff_output__

COUNT=0
FAILURES=0
while ( true ); do
    COUNT=$(expr $COUNT + 1)
    echo Starting run \#$COUNT on $(date). $FAILURES failures so far.

    npm run cy -- $*

    if [ $? -ne 0 ]; then
        FAILURES=$(expr $FAILURES + 1)
        echo Run failure \#$FAILURES on run \#$COUNT on $(date)

        # Comment this out to run forever but will keep a count of failures:
        break
    fi
done
