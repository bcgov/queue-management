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

from ..models.channel import Channel
from ..models.citizen import Citizen
from ..models.csr import CSR
from ..models.office import Office
from ..models.role import Role
from ..models.service import Service
from ..models.smartboard import SmartBoard
from snowplow_tracker import Subject, Tracker, Emitter
from snowplow_tracker import SelfDescribingJson
import os

class SnowPlow():

    sp_endpoint = os.getenv("THEQ_SNOWPLOW_ENDPOINT", "spm.gov.bc.ca")
    sp_appid = os.getenv("THEQ_SNOWPLOW_APPID", "CFMS")
    sp_namespace = os.getenv("THEQ_SNOWPLOW_NAMESPACE", "CFMS_dev")

    @staticmethod
    def add_citizen(new_citizen, csr):

        # print("==> SP: addcitizen");
        # print("    --> SP endpoint:  " + SnowPlow.sp_endpoint);
        # print("    --> SP appid:     " + SnowPlow.sp_appid);
        # print("    --> SP namespace: " + SnowPlow.sp_namespace);

        print("==> SP: addcitizen")

        # Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter("spm.gov.bc.ca")
        # e = Emitter(SnowPlow.sp_endpoint, on_failure=SnowPlow.failure)
        t = Tracker(e, encode_base64=False, app_id = "CFMS", namespace="CFMS_dev")

        # Set up contexts for the call.
        citizen = SnowPlow.get_citizen(new_citizen.citizen_id, 1, True)
        office = SnowPlow.get_office(new_citizen.office_id)
        agent = SnowPlow.get_csr(csr)

        # the addcitizen event has no parameters of its own so we pass an empty array "{}"
        addcitizen = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0', {})

        # make the call
        t.track_self_describing_event(addcitizen, [citizen, office, agent])

    @staticmethod
    def choose_service(service_request, csr, snowplow_event):

        print("==> SP: " + snowplow_event)

        # Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter(SnowPlow.sp_endpoint, on_failure=SnowPlow.failure)
        t = Tracker(e, encode_base64=False, app_id = SnowPlow.sp_appid, namespace=SnowPlow.sp_namespace)

        # Set up the contexts for the call.
        citizen = SnowPlow.get_citizen(service_request.citizen_id, service_request.quantity, False)
        office = SnowPlow.get_office(csr.office_id)
        agent = SnowPlow.get_csr(csr)

        #  The choose service event has parameters, needs to be built.
        chooseservice = SnowPlow.get_service(service_request)

        #  Make the call.
        t.track_self_describing_event(chooseservice, [citizen, office, agent])

    @staticmethod
    def snowplow_event(service_request, csr, schema, citizen_id = 0):

        print("==> SP: " + schema)

        #  Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter(SnowPlow.sp_endpoint, on_failure=SnowPlow.failure)
        t = Tracker(e, encode_base64=False, app_id = SnowPlow.sp_appid, namespace=SnowPlow.sp_namespace)

        #  If you have a service_request, get citizen ID from it.
        if (service_request is not None):
            citizen_id = service_request.citizen_id
            quantity = service_request.quantity
        else:
            quantity = 1

        #  Set up the contexts for the call.
        citizen = SnowPlow.get_citizen(citizen_id, quantity, False)
        office = SnowPlow.get_office(csr.office_id)
        agent = SnowPlow.get_csr(csr)

        #  Initialize schema version.
        schema_version = "1-0-0"

        #  If finish or hold events, parameters need to be built.
        if (schema == "finish"):
            snowplow_event = SnowPlow.get_finish(service_request.quantity)

        elif (schema == "hold"):
            snowplow_event = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/hold/jsonschema/1-0-0',
                                                {"time": 0})

        #  Most Snowplow events don't have parameters, so don't have to be built.
        else:
            snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

        # snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

        #  Make the call.
        t.track_self_describing_event(snowplow_event, [citizen, office, agent])

    @staticmethod
    def success(count):
        print("####> " + str(count) + " events sent successfully!")

    @staticmethod
    def failure(count, failed):
        print("###################  " + str(count) + " events sent successfuly.  Events below failed:")
        for event_dict in failed:
            print(event_dict)

    @staticmethod
    def get_citizen(id, quantity, add_flag):

        #  Set up citizen variables.
        if add_flag:
            citizen_qtxn = False
        else:
            citizen_obj = Citizen.query.get(id)
            citizen_qtxn = (citizen_obj.qt_xn_citizen_ind == 1)

        # #  Display citizen context info.
        # print("    --> Citizen")
        # print("        --> ID:                " + str(id))
        # print("        --> quantity:          " + str(quantity))
        # print("        --> quick txn:         " + str(citizen_qtxn))

        # Set up the citizen context.
        citizen = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/citizen/jsonschema/3-0-0',
                                      {"client_id": id, "service_count": quantity,
                                       "quick_txn": citizen_qtxn})

        return citizen

    @staticmethod
    def get_office(id):

        #  Set up office variables.
        curr_office = Office.query.get(id)
        office_num = curr_office.office_number
        my_board = SmartBoard.query.get(curr_office.sb_id)
        office_type = "non-reception"
        if (my_board.sb_type == "callbyname") or (my_board.sb_type == "callbyticket"):
            office_type = "reception"

        # #  Display office context info.
        # print("    --> Office")
        # print("        --> office number:     " + str(office_num))
        # print("        --> office type:       " + office_type)

        #  Set up the office context.
        office = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/office/jsonschema/1-0-0',
                                     {"office_id": office_num, "office_type": office_type})

        return office

    @staticmethod
    def get_csr(csr):

        #  Set up the CSR variables.
        role_obj = Role.query.get(csr.role_id)
        role_name = role_obj.role_code
        csr_qtxn = (csr.qt_xn_csr_ind == 1)

        # #  Display the CSR variables.
        # print("    --> CSR")
        # print("        --> CSR ID:            " + str(csr.csr_id))
        # print("        --> CSR role:          " + role_name)
        # print("        --> CSR qtxn:          " + str(csr_qtxn))

        #  Set up the CSR context.
        agent = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/agent/jsonschema/2-0-0',
                                   {"agent_id": csr.csr_id, "role": role_name, "quick_txn": csr_qtxn})

        return agent

    @staticmethod
    def get_service(service_request):

        #  Set up the Service variables.
        pgm_id = service_request.service.parent_id
        svc_id = service_request.service_id
        svc_code = service_request.service.service_code
        svc_name = service_request.service.service_name
        parent = Service.query.get(pgm_id)
        pgm_code = parent.service_code
        pgm_name = parent.service_name
        channel = Channel.query.get(service_request.channel_id)
        channel_name = channel.channel_name
        snowplow_channel = ""

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

        # #  Display the service variables.
        # print("    --> Service")
        # print("        --> Channel            " + snowplow_channel)
        # print("        --> Program code:      " + pgm_code)
        # print("        --> Program:           " + pgm_name)
        # print("        --> Service code:      " + svc_code)
        # print("        --> Service:           " + svc_name)

        # for chooseservices, we build a JSON array and pass it
        chooseservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/chooseservice/jsonschema/3-0-0',
                                           {"channel": snowplow_channel, "program_id": svc_code, "parent_id": pgm_code,
                                            "program_name": pgm_name,
                                            "transaction_name": svc_name})

        return chooseservice

    @staticmethod
    def get_finish(svc_quantity):
        finishservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/finish/jsonschema/1-0-0',
                                           {"inaccurate_time": False, "count": svc_quantity})
        return finishservice
