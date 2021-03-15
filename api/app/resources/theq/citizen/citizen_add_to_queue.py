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

from datetime import datetime
from flask import g, request
from pprint import pprint
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, Office
from app.models.theq import SRState
from app.schemas.theq import CitizenSchema
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt
from app.utilities.email import get_walkin_spot_confirmation_email_contents, send_email, generate_ches_token
from app.utilities.sms import send_walkin_spot_confirmation_sms


@api.route("/citizens/<int:id>/add_to_queue/", methods=["POST"])
class CitizenAddToQueue(Resource):

    citizen_schema = CitizenSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self, id):
        csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
        citizen = Citizen.query.filter_by(citizen_id=id).first()
        active_service_request = citizen.get_active_service_request()

        my_print("==> POST /citizens/" + str(citizen.citizen_id) + '/add_to_queue, Ticket: ' + citizen.ticket_number)

        if active_service_request is None:
            return {"message": "Citizen has no active service requests"}

        #  Figure out what Snowplow call to make.  Default is addtoqueue
        snowplow_call = "addtoqueue"
        if len(citizen.service_reqs) != 1 or len(active_service_request.periods) != 1:
            active_period = active_service_request.get_active_period()
            if active_period.ps.ps_name == "Invited":
                snowplow_call = "queuefromprep"
            elif active_period.ps.ps_name == "Being Served":
                snowplow_call = "returntoqueue"
            else:
                #  TODO:  Put in a Feedback Slack/Service now call here.
                return {"message": "Invalid citizen/period state. "}

        active_service_request.add_to_queue(csr, snowplow_call)

        pending_service_state = SRState.get_state_by_name("Pending")
        active_service_request.sr_state_id = pending_service_state.sr_state_id
        # send walkin spot confirmation
        try:
            if citizen.notification_phone or citizen.notification_email:
                # TODO: code/function call to send first sms/email confirmation
                update_table = False
                try:
                    # TODO: Preapre tiny url and replace below url
                    url = "http://localhost:8081/queue"
                    # email
                    email_sent = False
                    if citizen.notification_email:
                        ches_token = generate_ches_token()
                        officeObj = Office.find_by_id(citizen.office_id)
                        pprint('Sending email for walk in spot confirmations')
                        email_sent = get_walkin_spot_confirmation_email_contents(citizen, url, officeObj)
                    # SMS  
                    sms_sent = False
                    if citizen.notification_phone:
                        sms_sent = send_walkin_spot_confirmation_sms(citizen, url, request.headers['Authorization'].replace('Bearer ', ''))
                    if email_sent:
                        # status = send_email(ches_token, *email_sent)
                        update_table = True
                    if sms_sent:
                        update_table = True
                except Exception as exc:
                    pprint(f'Error on token generation - {exc}')
                    update_table = False
                if update_table:
                    citizen.reminder_flag = 0
                    citizen.notification_sent_time = datetime.utcnow()
        except Exception as err:
            logging.error('{}'.format(str(err)))
            pprint(err)

        db.session.add(citizen)
        db.session.commit()

        socketio.emit('update_customer_list', {}, room=csr.office_id)
        socketio.emit('citizen_invited', {}, room='sb-%s' % csr.office.office_number)
        result = self.citizen_schema.dump(citizen)
        socketio.emit('update_active_citizen', result, room=csr.office_id)
        
        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 200
