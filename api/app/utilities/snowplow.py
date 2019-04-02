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

from app.models.theq.channel import Channel
from app.models.theq.citizen import Citizen
from app.models.theq.csr import CSR
from app.models.theq.office import Office
from app.models.theq.role import Role
from app.models.theq.service import Service
from app.models.theq.smartboard import SmartBoard
import os
import http.client
import time
import json
from pprint import pprint

class SnowPlow():

    sp_endpoint = os.getenv("THEQ_SNOWPLOW_ENDPOINT", "")
    sp_appid = os.getenv("THEQ_SNOWPLOW_APPID", "")
    sp_namespace = os.getenv("THEQ_SNOWPLOW_NAMESPACE", "")
    sp_env = os.getenv("THEQ_SNOWPLOW_ENV", "test")
    sp_host = os.getenv("THEQ_SNOWPLOW_ROUTE", "")
    call_snowplow_flag = (os.getenv("THEQ_SNOWPLOW_CALLFLAG", "False")).upper() == "TRUE"
    if (not sp_endpoint.strip()) or (not sp_appid.strip()) \
            or (not sp_namespace.strip()) or (not sp_host.strip()):
        call_snowplow_flag = False

    # Prepare the event requirements
    sp_config = {
        'env': sp_env,  # test or prod
        'namespace': sp_namespace,
        'app_id': sp_appid
    }

    print("==> In Slowplow class")
    print("    --> CALLFLAG:  " + str(call_snowplow_flag))
    print("    --> ENV:       " + sp_env)
    print("    --> ENDPOINT:  " + sp_endpoint)
    print("    --> HOST:      " + sp_host)
    print("    --> APPID:     " + sp_appid)
    print("    --> NAMESPACE: " + sp_namespace)

    @staticmethod
    def add_citizen(new_citizen, csr):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            # Set up contexts for the call.
            citizen_obj = Citizen.query.get(new_citizen.citizen_id)
            citizen_dict = SnowPlow.get_citizen_dict(citizen_obj, True)
            office_dict = SnowPlow.get_office_dict(new_citizen.office_id)
            agent_dict = SnowPlow.get_csr_dict(csr)

            # the addcitizen event has no parameters of its own so we pass an empty array "{}"
            addcitizen_schema = 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0'
            addcitizen_data = {}

            # make the call
            SnowPlow.make_tracking_call_dict(addcitizen_schema, citizen_dict, office_dict, agent_dict, addcitizen_data)

    @staticmethod
    def choose_service(service_request, csr, snowplow_event):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            # Set up the contexts for the call.
            citizen_obj = Citizen.query.get(service_request.citizen_id)
            current_sr_number = service_request.sr_number
            citizen_dict = SnowPlow.get_citizen_dict(citizen_obj, False, svc_number = current_sr_number)
            office_dict = SnowPlow.get_office_dict(csr.office_id)
            agent_dict = SnowPlow.get_csr_dict(csr)

            #  The choose service event has parameters, needs to be built.
            chooseservice_schema = 'iglu:ca.bc.gov.cfmspoc/chooseservice/jsonschema/3-0-0'
            chooseservice_dict = SnowPlow.get_service_dict(service_request)

            SnowPlow.make_tracking_call_dict(chooseservice_schema, citizen_dict, office_dict,
                                             agent_dict, chooseservice_dict)

    @staticmethod
    def snowplow_event(citizen_id, csr, schema, period_count = 0, quantity = 0, current_sr_number = 0):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            #  Set up the contexts for the call.
            citizen_obj = Citizen.query.get(citizen_id)
            citizen_dict = SnowPlow.get_citizen_dict(citizen_obj, False, svc_number = current_sr_number)
            office_dict = SnowPlow.get_office_dict(csr.office_id)
            agent_dict = SnowPlow.get_csr_dict(csr)

            #  Initialize schema version.
            schema_version = "1-0-0"

            if (schema == "finish"):
                event_schema = 'iglu:ca.bc.gov.cfmspoc/finish/jsonschema/2-0-0'
                event_data = {
                    'inaccurate_time': (citizen_obj.accurate_time_ind != 1),
                    'quantity': quantity
                }

            elif (schema == 'finishstopped'):
                event_schema = 'iglu:ca.bc.gov.cfmspoc/finishstopped/jsonschema/1-0-0'
                event_data = {
                    'quantity': quantity
                }

            elif schema == "hold":
                event_schema = 'iglu:ca.bc.gov.cfmspoc/hold/jsonschema/1-0-0'
                event_data = {
                    'time': 0
                }

            elif schema[:5] == "left/":
                event_schema = 'iglu:ca.bc.gov.cfmspoc/customerleft/jsonschema/2-0-0'
                event_data = {
                    'leave_status': schema[5:]
                }

            #  Most Snowplow events don't have parameters, so don't have to be built.
            else:
                event_schema = 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version
                event_data = {}

            #  Make the call.
            SnowPlow.make_tracking_call_dict(event_schema, citizen_dict, office_dict, agent_dict, event_data)

    @staticmethod
    def failure(count, failed):
        print("###################  " + str(count) + " events sent successfuly.  Events below failed:")
        for event_dict in failed:
            print(event_dict)

    @staticmethod
    def get_citizen_dict(citizen_obj, add_flag, close_previous = False, svc_number = 1):

        #  Set up citizen variables.
        if add_flag:
            citizen_qtxn = False
        else:
            citizen_qtxn = (citizen_obj.qt_xn_citizen_ind == 1)

        # Set up the citizen context.
        citizen_dict = {
            'data': {
                'client_id': citizen_obj.citizen_id,
                'service_count': svc_number,
                'quick_txn': citizen_qtxn
            },
            'schema': 'iglu:ca.bc.gov.cfmspoc/citizen/jsonschema/3-0-0'
        }

        return citizen_dict

    @staticmethod
    def get_office_dict(id):

        #  Set up office variables.
        curr_office = Office.query.get(id)
        office_num = curr_office.office_number
        my_board = SmartBoard.query.get(curr_office.sb_id)
        office_type = "non-reception"
        if (my_board.sb_type == "callbyname") or (my_board.sb_type == "callbyticket"):
            office_type = "reception"

        office_dict = {
            'data':
            {
                'office_id': office_num,
                'office_type': office_type
            },
            'schema':'iglu:ca.bc.gov.cfmspoc/office/jsonschema/1-0-0'
        }

        return office_dict

    @staticmethod
    def get_csr_dict(csr):

        #  If csr is a receptionist, that is their role.
        if csr.receptionist_ind == 1:
            role_name = "Reception"

        #  If not a receptionist, get role from their role id
        else:
            role_obj = Role.query.get(csr.role_id)
            role_name = role_obj.role_code

        csr_qtxn = (csr.qt_xn_csr_ind == 1)

        agent_dict = {
            'data':
            {
                'agent_id': csr.csr_id,
                'role': role_name,
                'quick_txn': csr_qtxn
            },
            'schema':'iglu:ca.bc.gov.cfmspoc/agent/jsonschema/2-0-0'
        }

        return agent_dict

    @staticmethod
    def get_service_dict(service_request):

        #  Set up the Service variables.
        pgm_id = service_request.service.parent_id
        svc_code = service_request.service.service_code
        svc_name = service_request.service.service_name
        parent = Service.query.get(pgm_id)
        pgm_code = parent.service_code
        pgm_name = parent.service_name
        channel = Channel.query.get(service_request.channel_id)
        channel_name = channel.channel_name

        #  Translate channel name to old versions, to avoid major Snowplow changes
        if (channel_name == 'In Person'):
            snowplow_channel = "in-person"
        elif (channel_name == 'Phone'):
            snowplow_channel = "phone"
        elif (channel_name == 'Back Office'):
            snowplow_channel = "back-office"
        elif (channel_name == 'Email/Fax/Mail'):
            snowplow_channel = "email-fax-mail"
        elif (channel_name == 'CATs Assist'):
            snowplow_channel = "cats-assist"
        elif (channel_name == 'Mobile Assist'):
            snowplow_channel = "mobile-assist"
        else:
            snowplow_channel = "sms"

        chooseservice_dict = {
            'channel': snowplow_channel,
            'program_id': svc_code,
            'parent_id': pgm_code,
            'program_name': pgm_name,
            'transaction_name': svc_name
        }

        return chooseservice_dict

    # time of event as an epoch timestamp in milliseconds
    @staticmethod
    def event_timestamp():
        # time.time() returns the time in seconds with 6 decimal places of precision
        return int(round(time.time() * 1000))

    # schema is a string to the iglu:ca.bc.gov schema for this event
    # context is the list of contexts as dictionaries for this event
    # data is a dictionary describing this events data
    @staticmethod
    def event(schema, contexts, data, configuration):
        post_body = configuration
        post_body['dvce_created_tstamp'] = SnowPlow.event_timestamp()
        post_body['event_data_json'] = {
            'contexts': contexts,
            'data': data,
            'schema': schema
        }
        return post_body

    # make the POST call that contains the event data
    @staticmethod
    def post_event(json_event):
        # Make the connection
        conn = http.client.HTTPSConnection(SnowPlow.sp_host)

        # Prepare the headers
        headers = {'Content-type': 'application/json'}

        # Send a post request containing the event as JSON in the body
        conn.request('POST', '/post', json_event, headers)

        # Recieve the response
        try:
            response = conn.getresponse()
        except http.client.ResponseNotReady as e:
            print("==> Snowplow pod ResponseNotReady Exception raised")
            # sys.exit(1)
        # Print the response, if it is not 200.
        if response.status != 200:
            print("==> Snowplow pod did not respond with status of 200")
            print(response.status, response.reason)

    @staticmethod
    def make_tracking_call_dict(schema, citizen_dict, office_dict, agent_dict, data):

        #  Create the contexts from input dictionaries.
        contexts = [citizen_dict, office_dict, agent_dict]

        # create example event
        example_event = SnowPlow.event(schema, contexts, data, SnowPlow.sp_config)

        # Create a JSON object from the event dictionary
        json_event = json.dumps(example_event)

        print("===========> Snowplow call <==================")
        pprint(example_event)
        print("==============================================")

        # POST the event to the Analytics service
        SnowPlow.post_event(json_event)
