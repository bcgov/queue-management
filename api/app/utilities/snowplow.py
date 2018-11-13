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
            citizen = SnowPlow.get_citizen(citizen_obj, True)
            office = SnowPlow.get_office(new_citizen.office_id)
            agent = SnowPlow.get_csr(csr)

            # the addcitizen event has no parameters of its own so we pass an empty array "{}"
            addcitizen = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addcitizen/jsonschema/1-0-0', {})

            # make the call
            t.track_self_describing_event(addcitizen, [citizen, office, agent])

    @staticmethod
    def choose_service(service_request, csr, snowplow_event):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            # Set up the contexts for the call.
            citizen_obj = Citizen.query.get(service_request.citizen_id)
            citizen = SnowPlow.get_citizen(citizen_obj, False)
            office = SnowPlow.get_office(csr.office_id)
            agent = SnowPlow.get_csr(csr)

            #  The choose service event has parameters, needs to be built.
            chooseservice = SnowPlow.get_service(service_request)

            #  If an additionalservice event, add "bogus" SP events before.
            if snowplow_event == "additionalservice":
                prev_citizen = SnowPlow.get_citizen(citizen_obj, False, True)
                sp_event = SnowPlow.get_finish(service_request.quantity, citizen_obj.accurate_time_ind)
                t.track_self_describing_event(sp_event, [prev_citizen, office, agent])
                sp_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/additionalservice/jsonschema/1-0-0', {})
                t.track_self_describing_event(sp_event, [citizen, office, agent])

            #  Make the call.
            t.track_self_describing_event(chooseservice, [citizen, office, agent])

            #  If an additionalservice event, add "bogus" SP events after.
            if snowplow_event == "additionalservice":
                #  Add invitecitizen, beginservice after chooseservice
                sp_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/invitecitizen/jsonschema/1-0-0', {})
                t.track_self_describing_event(sp_event, [citizen, office, agent])
                sp_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/beginservice/jsonschema/1-0-0', {})
                t.track_self_describing_event(sp_event, [citizen, office, agent])

    @staticmethod
    def snowplow_event(citizen_id, csr, schema, period_count = 0, quantity = 0):

        #  Make sure you want to track calls.
        if SnowPlow.call_snowplow_flag:

            #  Set up the contexts for the call.
            citizen_obj = Citizen.query.get(citizen_id)
            citizen = SnowPlow.get_citizen(citizen_obj, False)
            office = SnowPlow.get_office(csr.office_id)
            agent = SnowPlow.get_csr(csr)

            #  Initialize schema version.
            schema_version = "1-0-0"

            #  If finish or hold events, parameters need to be built.
            if schema == "finish":
                snowplow_event = SnowPlow.get_finish(quantity, citizen_obj.accurate_time_ind)

            elif schema == "hold":
                snowplow_event = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/hold/jsonschema/1-0-0',
                                                {"time": 0})

            #  If begin service direct from choose service, extra Snowplow events needed.
            elif (schema == "beginservice") and (period_count == 2):

                #  Add "bogus" add to queue and invitecitizen events.
                sp_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/addtoqueue/jsonschema/1-0-0', {})
                t.track_self_describing_event(sp_event, [citizen, office, agent])
                sp_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/invitecitizen/jsonschema/1-0-0', {})
                t.track_self_describing_event(sp_event, [citizen, office, agent])

                #  Create "real" beginservice event.
                snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

            #  Most Snowplow events don't have parameters, so don't have to be built.
            else:
                snowplow_event = SelfDescribingJson( 'iglu:ca.bc.gov.cfmspoc/' + schema + '/jsonschema/' + schema_version, {})

            #  Make the call.
            t.track_self_describing_event(snowplow_event, [citizen, office, agent])

    @staticmethod
    def failure(count, failed):
        print("###################  " + str(count) + " events sent successfuly.  Events below failed:")
        for event_dict in failed:
            print(event_dict)

    @staticmethod
    def get_citizen(citizen_obj, add_flag, close_previous = False):

        #  Set up citizen variables.
        if add_flag:
            citizen_qtxn = False
            svc_count = citizen_obj.service_count
        else:
            citizen_qtxn = (citizen_obj.qt_xn_citizen_ind == 1)
            svc_count = citizen_obj.service_count

        #  If closing previous service, subtract 1 from svc_count
        if close_previous:
            svc_count = citizen_obj.service_count - 1

        # Set up the citizen context.
        citizen = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/citizen/jsonschema/3-0-0',
                                      {"client_id": citizen_obj.citizen_id, "service_count": svc_count,
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

        #  Set up the CSR context.
        agent = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/agent/jsonschema/2-0-0',
                                   {"agent_id": csr.csr_id, "role": role_name, "quick_txn": csr_qtxn})

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
                                           {"channel": snowplow_channel, "program_id": svc_code, "parent_id": pgm_code,
                                            "program_name": pgm_name,
                                            "transaction_name": svc_name})

        return chooseservice

    @staticmethod
    def get_finish(svc_quantity, accurate_time):
        inaccurate_flag = accurate_time != 1
        finishservice = SelfDescribingJson('iglu:ca.bc.gov.cfmspoc/finish/jsonschema/1-0-0',
                                           {"inaccurate_time": inaccurate_flag, "count": svc_quantity})
        return finishservice


# Set up core Snowplow environment
if SnowPlow.call_snowplow_flag:
    s = Subject()  # .set_platform("app")
    e = AsyncEmitter(SnowPlow.sp_endpoint, on_failure=SnowPlow.failure, protocol="https")
    t = Tracker(e, encode_base64=False, app_id=SnowPlow.sp_appid, namespace=SnowPlow.sp_namespace)
