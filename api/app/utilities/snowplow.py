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
from snowplow_tracker import Subject, Tracker, AsyncEmitter
from snowplow_tracker import SelfDescribingJson
import os

class SnowPlow():

    sp_endpoint = os.getenv("THEQ_SNOWPLOW_ENDPOINT", "")
    sp_appid = os.getenv("THEQ_SNOWPLOW_APPID", "")
    sp_namespace = os.getenv("THEQ_SNOWPLOW_NAMESPACE", "")
    call_snowplow_flag = (os.getenv("THEQ_SNOWPLOW_CALLFLAG", "False")).upper() == "TRUE"
    if (not sp_endpoint.strip()) or (not sp_appid.strip()) or (not sp_namespace.strip()):
        call_snowplow_flag = False

    @staticmethod
    def add_citizen(new_citizen, csr):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            # Set up contexts for the call.
            citizen_obj = Citizen.query.get(new_citizen.citizen_id)
            citizen = SnowPlow.get_citizen(citizen_obj, csr.counter.counter_name)
            office = SnowPlow.get_office(new_citizen.office_id)
            agent = SnowPlow.get_csr(csr)

            # the addcitizen event has no parameters of its own so we pass an empty array "{}"
            addcitizen = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0', {})

            # make the call
            SnowPlow.make_tracking_call(addcitizen, citizen, office, agent)

    @staticmethod
    def choose_service(service_request, csr, snowplow_event):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            # Set up the contexts for the call.
            citizen_obj = Citizen.query.get(service_request.citizen_id)
            current_sr_number = service_request.sr_number
            citizen = SnowPlow.get_citizen(citizen_obj, csr.counter.counter_name, svc_number = current_sr_number)
            office = SnowPlow.get_office(csr.office_id)
            agent = SnowPlow.get_csr(csr)

            #  The choose service event has parameters, needs to be built.
            chooseservice = SnowPlow.get_service(service_request)

            SnowPlow.make_tracking_call(chooseservice, citizen, office, agent)

    @staticmethod
    def snowplow_event(citizen_id, csr, schema, period_count = 0, quantity = 0, current_sr_number = 0):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            #  Set up the contexts for the call.
            citizen_obj = Citizen.query.get(citizen_id)
            citizen = SnowPlow.get_citizen(citizen_obj, csr.counter.counter_name, svc_number = current_sr_number)
            office = SnowPlow.get_office(csr.office_id)
            agent = SnowPlow.get_csr(csr)

            #  Initialize schema version.
            schema_version = "1-0-0"

            #  If finish or hold events, parameters need to be built.
            if (schema == "finish") or (schema == "finishstopped"):
                snowplow_event = SnowPlow.get_finish(quantity, citizen_obj.accurate_time_ind, schema)

            elif schema == "hold":
                snowplow_event = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/hold/jsonschema/1-0-0',
                                                {"time": 0})

            elif schema[:5] == "left/":
                snowplow_event = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/customerleft/jsonschema/2-0-0',
                                                    {"leave_status": schema[5:]})

            #  Most Snowplow events don't have parameters, so don't have to be built.
            else:
                snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

            #  Make the call.
            SnowPlow.make_tracking_call(snowplow_event, citizen, office, agent)

    @staticmethod
    def snowplow_appointment(citizen_obj, csr, appointment, schema):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            #  Set up the contexts for the call.
            citizen = SnowPlow.get_citizen(citizen_obj, csr.counter.counter_name)
            office = SnowPlow.get_office(csr.office_id)
            agent = SnowPlow.get_csr(csr)

            #  Initialize appointment schema version.
            snowplow_event = SnowPlow.get_appointment(appointment)

            #  Make the call.
            SnowPlow.make_tracking_call(snowplow_event, citizen, office, agent)

    @staticmethod
    def failure(count, failed):
        print("###################  " + str(count) + " events sent successfuly.  Events below failed:")
        for event_dict in failed:
            print(event_dict)

    @staticmethod
    def get_citizen(citizen_obj, counter_name, svc_number = 1):

        citizen_type = counter_name
        if citizen_obj.counter is not None:
            citizen_type = citizen_obj.counter.counter_name

        # Set up the citizen context.
        citizen = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/citizen/jsonschema/4-0-0',
                                      {"client_id": citizen_obj.citizen_id, "service_count": svc_number,
                                       "counter_type": citizen_type})

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

        #  Set up the office context.
        office = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/office/jsonschema/1-0-0',
                                     {"office_id": office_num, "office_type": office_type})

        return office

    @staticmethod
    def get_csr(csr):

        #  If csr is a receptionist, that is their role.
        if csr.receptionist_ind == 1:
            role_name = "Reception"

        #  If not a receptionist, get role from their role id
        else:
            role_obj = Role.query.get(csr.role_id)
            role_name = role_obj.role_code

        csr_qtxn = (csr.qt_xn_csr_ind == 1)

        #  Set up the CSR context.
        agent = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/agent/jsonschema/3-0-0',
                                   {"agent_id": csr.csr_id, "role": csr.role.role_code,
                                    "counter_type": csr.counter.counter_name})

        return agent

    @staticmethod
    def get_service(service_request):

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

        # for chooseservices, we build a JSON array and pass it
        chooseservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/chooseservice/jsonschema/3-0-0',
                                           {"channel": snowplow_channel,
                                            "program_id": svc_code,
                                            "parent_id": pgm_code,
                                            "program_name": pgm_name,
                                            "transaction_name": svc_name})

        return chooseservice

    @staticmethod
    def get_finish(svc_quantity, accurate_time, schema):
        inaccurate_flag = (accurate_time != 1) and (schema == "finish")
        if schema == "finish":

            finishservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/finish/jsonschema/2-0-0',
                                               {"inaccurate_time": inaccurate_flag, "quantity": svc_quantity})
        else:
            finishservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/finishstopped/jsonschema/1-0-0',
                                               {"quantity": svc_quantity})

        return finishservice

    @staticmethod
    def get_appointment(appointment):

        print("==> In appointment module")
        print("    --> ID:        " + str(appointment.appointment_id))
        print("    --> Start:     " + str(appointment.start_time))
        print("    --> End:       " + str(appointment.end_time))
        print("    --> Pgm ID:    " + str(appointment.service.service_code))
        print("    --> Parent ID: " + str(appointment.service.parent.service_code))
        print("    --> Pgm Name:  " + str(appointment.service.parent.service_code))
        print("    --> Txn Name:  " + str(appointment.service.service_name))

        appointment = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/appointment_create/jsonschema/1-0-0',
                                         {"appointment_id": appointment.appointment_id,
                                          "appointment_start_timestamp": str(appointment.start_time),
                                          "appointment_end_timestamp": str(appointment.end_time),
                                          "program_id": appointment.service.service_code,
                                          "parent_id": appointment.service.parent.service_code,
                                          "program_name": appointment.service.parent.service_name,
                                          "transaction_name": appointment.service.service_name})

        return appointment

    @staticmethod
    def make_tracking_call(schema, citizen, office, agent):
        t.track_self_describing_event(schema, [citizen, office, agent])

# Set up core Snowplow environment
if SnowPlow.call_snowplow_flag:
    s = Subject()  # .set_platform("app")
    e = AsyncEmitter(SnowPlow.sp_endpoint, on_failure=SnowPlow.failure, protocol="https")
    t = Tracker(e, encode_base64=False, app_id=SnowPlow.sp_appid, namespace=SnowPlow.sp_namespace)
