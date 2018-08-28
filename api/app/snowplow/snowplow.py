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

class SnowPlow():

    @staticmethod
    def add_citizen(new_citizen, csr):

        print("==> SP: add_citizen");

        # Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter("spm.gov.bc.ca")
        t = Tracker(e, encode_base64=False, app_id = 'CFMS', namespace="CFMS_dev")

        # Set up contexts for the call.
        citizen = SnowPlow.get_citizen(new_citizen.citizen_id, 1, True)
        office = SnowPlow.get_office(new_citizen.office_id)
        agent = SnowPlow.get_csr(csr)

        # the addcitizen event has no parameters of its own so we pass an empty array "{}"
        addcitizen = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0', {})

        # make the call
        t.track_self_describing_event(addcitizen, [citizen, office, agent])

    @staticmethod
    def choose_service(service_request, csr):

        print("==> SP: choose_service")

        # Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter("spm.gov.bc.ca")
        t = Tracker(e, encode_base64=False, app_id = 'CFMS', namespace="CFMS_dev")

        # Set up the contexts for the call.
        citizen = SnowPlow.get_citizen(service_request.citizen_id, service_request.quantity, False)
        office = SnowPlow.get_office(csr.office_id)
        agent = SnowPlow.get_csr(csr)

        #  The choose service event has parameters, needs to be built.
        chooseservice = SnowPlow.get_service(service_request)

        #  Make the call.
        t.track_self_describing_event(chooseservice, [citizen, office, agent])

    @staticmethod
    def snowplow_event(service_request, csr, schema):

        print("==> SP: Snowplow event: " + schema)

        #  Set up core Snowplow environment
        s = Subject()#.set_platform("app")
        e = Emitter("spm.gov.bc.ca")
        t = Tracker(e, encode_base64=False, app_id = 'CFMS', namespace="CFMS_dev")

        #  Set up the contexts for the call.
        citizen = SnowPlow.get_citizen(service_request.citizen_id, service_request.quantity, False)
        office = SnowPlow.get_office(csr.office_id)
        agent = SnowPlow.get_csr(csr)

        #  Initialize schema version.
        schema_version = "1-0-0"

        #  The choose service event has parameters, needs to be built.
        snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

        #  Make the call.
        t.track_self_describing_event(snowplow_event, [citizen, office, agent])


        # # the addcitizen event has no parameters of its own so we pass an empty array "{}"
        # addcitizen = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0', {})
        #
        # # make the call
        # t.track_self_describing_event(addcitizen, [citizen, office, agent])


    @staticmethod
    def get_citizen(id, quantity, add_flag):

        #  Set up citizen variables.
        if add_flag:
            citizen_qtxn = False
        else:
            citizen_obj = Citizen.query.get(id)
            citizen_qtxn = (citizen_obj.qt_xn_citizen_ind == 1)

        #  Display citizen context info.
        print("    --> Citizen")
        print("        --> ID:                " + str(id))
        print("        --> quantity:          " + str(quantity))
        print("        --> quick txn:         " + str(citizen_qtxn))

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

        #  Display office context info.
        print("    --> Office")
        print("        --> office number:     " + str(office_num))
        print("        --> office type:       " + office_type)

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

        #  Display the CSR variables.
        print("    --> CSR")
        print("        --> CSR ID:            " + str(csr.csr_id))
        print("        --> CSR role:          " + role_name)
        print("        --> CSR qtxn:          " + str(csr_qtxn))

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

        #  Display the service variables.
        print("    --> Service")
        print("        --> Channel            " + channel_name)
        print("        --> Program code:      " + pgm_code)
        print("        --> Program:           " + pgm_name)
        print("        --> Service code:      " + svc_code)
        print("        --> Service:           " + svc_name)

        # for chooseservices, we build a JSON array and pass it
        chooseservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/chooseservice/jsonschema/2-0-0',
                                           {"channel": "in-person", "program_id": svc_id, "parent_id": pgm_id,
                                            "program_name": pgm_name,
                                            "transaction_name": svc_name})

        return chooseservice