'''
Manages the database with commands for:
    db: apply standard database migration steps.
    migrate: shortcut for "db upgrade".
    bootstrap: deletes all data from the database and re-populates with
        data suitable for development or demos.

Usage:
    python manage.py db <arguments>
    python manage.py migrate
    python manage.py bootstrap # ***will wipe your database***
'''

import logging

from flask_script import Command, Manager
from flask_migrate import Migrate, MigrateCommand, upgrade

from qsystem import db, application
from app.models import theq, bookings

migrate = Migrate(application, db)
manager = Manager(application)


class Bootstrap(Command):
    '''
    Sets up the database with enough information to do development or
    run demos.
    '''

    def run(self):
        '''
        Bootstraps the database by deleting all table rows and
        populating with enough data to run the application for
        development or demos.
        '''

        logging.info('Clearing out all models')
        theq.Period.query.delete()
        theq.PeriodState.query.delete()
        theq.ServiceReq.query.delete()
        theq.SRState.query.delete()
        bookings.Appointment.query.delete()
        bookings.Booking.query.delete()
        bookings.Exam.query.delete()
        theq.Citizen.query.delete()
        theq.CitizenState.query.delete()
        theq.CSR.query.delete()
        theq.CSRState.query.delete()
        bookings.Booking.query.delete()
        bookings.ExamType.query.delete()
        bookings.Room.query.delete()
        bookings.Invigilator.query.delete()
        theq.TimeSlot.query.delete()
        theq.Office.query.delete()
        theq.SmartBoard.query.delete()
        theq.Counter.query.delete()
        theq.Role.query.delete()
        theq.Permission.query.delete()
        theq.Service.query.filter_by(actual_service_ind=1).delete()
        theq.Service.query.delete()
        theq.Channel.query.delete()
        bookings.Booking.query.delete()
        theq.Timezone.query.delete()

        logging.info('Starting to bootstrap data')

        # -- Channels --------------------------------------------------
        logging.info('--> Channels')
        db.session.add(theq.Channel(channel_name='In Person'))
        db.session.add(theq.Channel(channel_name='Phone'))
        db.session.add(theq.Channel(channel_name='Back Office'))
        db.session.add(theq.Channel(channel_name='Email/Fax/Mail'))
        db.session.add(theq.Channel(channel_name='CATs Assist'))
        db.session.add(theq.Channel(channel_name='Mobile Assist'))
        db.session.commit()

        # -- Roles -----------------------------------------------------
        logging.info('--> Roles')
        role_csr = theq.Role(
            role_code='CSR',
            role_desc='Customer Service Representative'
        )
        role_ga = theq.Role(
            role_code='GA',
            role_desc='Government Agent'
        )
        role3 = theq.Role(
            role_code='HELPDESK',
            role_desc='Help Desk Functions'
        )
        role4 = theq.Role(
            role_code='SUPPORT',
            role_desc='All Administrative Functions'
        )
        role5 = theq.Role(
            role_code='ANALYTICS',
            role_desc='Analytics Team to update Services per Office'
        )
        db.session.add(role_csr)
        db.session.add(role_ga)
        db.session.add(role3)
        db.session.add(role4)
        db.session.add(role5)
        db.session.commit()

        # -- Period States ---------------------------------------------
        logging.info('--> Period States')
        db.session.add(theq.PeriodState(
            ps_name='Waiting',
            ps_desc='Waiting in line to see a CSR, after a ticket has been '
            'created for them. The time they are in this state is the Citizen '
            'Wait Time.',
            ps_number=1
        ))
        db.session.add(theq.PeriodState(
            ps_name='Ticket Creation',
            ps_desc='A receptionist is creating a service request / ticket '
            'for the citizen. This is the first state a citizen will be in. '
            'The time they are in this state is the CSR prep time.',
            ps_number=2
        ))
        db.session.add(theq.PeriodState(
            ps_name='Invited',
            ps_desc='Has been called from the waiting area to be served. The '
            'time they are in this state is the time it takes them to walk '
            'from the waiting area, to the CSR, until the CSR starts to serve '
            'them.',
            ps_number=4
        ))
        db.session.add(theq.PeriodState(
            ps_name='Being Served',
            ps_desc='Is being served by a CSR. The time they are in this '
            'state is the Service time.',
            ps_number=7
        ))
        db.session.add(theq.PeriodState(
            ps_name='On hold',
            ps_desc='Has been placed on hold by a CSR. The time they are in '
            'this state is the Hold time.',
            ps_number=11
        ))
        db.session.commit()

        # -- Smart Boards ----------------------------------------------
        logging.info('--> Smart Boards')
        smartboard_call_name = theq.SmartBoard(sb_type='callbyname')
        smartboard_call_ticket = theq.SmartBoard(sb_type='callbyticket')
        smartboard_no_call = theq.SmartBoard(sb_type='nocallonsmartboard')
        db.session.add(smartboard_call_name)
        db.session.add(smartboard_call_ticket)
        db.session.add(smartboard_no_call)
        db.session.commit()

        # -- Citizen States --------------------------------------------
        logging.info('--> Citizen States')
        db.session.add(theq.CitizenState(
            cs_state_name='Active',
            cs_state_desc='Citizen is active, a ticket is being or has been '
            'created for them'
        ))
        db.session.add(theq.CitizenState(
            cs_state_name='Received Services',
            cs_state_desc='Citizen left after receiving services'
        ))
        db.session.add(theq.CitizenState(
            cs_state_name='Left before receiving services',
            cs_state_desc='Citizen left, after ticket creation, before '
            'service was started for them'
        ))
        db.session.add(theq.CitizenState(
            cs_state_name='Appointment booked',
            cs_state_desc='Citizen has booked an appointment'
        ))
        db.session.commit()

        # -- CSR States ------------------------------------------------
        logging.info('--> CSR States')
        csr_state_logout = theq.CSRState(
            csr_state_name='Logout',
            csr_state_desc='Logged out'
        )
        csr_state2 = theq.CSRState(
            csr_state_name='Login',
            csr_state_desc='Logged in'
        )
        csr_state3 = theq.CSRState(
            csr_state_name='Break',
            csr_state_desc='Currently on break'
        )
        csr_state4 = theq.CSRState(
            csr_state_name='Serving',
            csr_state_desc='Serving a citizen'
        )
        csr_state5 = theq.CSRState(
            csr_state_name='Back Office',
            csr_state_desc='Currently doing back office work'
        )
        db.session.add(csr_state_logout)
        db.session.add(csr_state2)
        db.session.add(csr_state3)
        db.session.add(csr_state4)
        db.session.add(csr_state5)
        db.session.commit()

        # -- Service Request States ------------------------------------
        logging.info('--> Service Request States')
        db.session.add(theq.SRState(
            sr_code='Pending',
            sr_state_desc='Service Request is pending, citizen has not '
            'started receiving services yet.'
        ))
        db.session.add(theq.SRState(
            sr_code='Active',
            sr_state_desc='Service Request is active. A citizen has '
            'started being served.'
        ))
        db.session.add(theq.SRState(
            sr_code='Complete',
            sr_state_desc='The service has been received for this Service '
            'Request.'
        ))
        db.session.commit()

        # -- Services (Categories) -------------------------------------
        logging.info('--> Services (Categories)')
        category_msp = theq.Service(
            service_code='MSP',
            service_name='MSP',
            service_desc='Medical Services Plan',
            prefix='A',
            display_dashboard_ind=0,
            actual_service_ind=0
        )
        category_ptax = theq.Service(
            service_code='PTAX',
            service_name='Property Tax',
            service_desc='Property Tax',
            prefix='A',
            display_dashboard_ind=0,
            actual_service_ind=0
        )
        category_back_office = theq.Service(
            service_code='Back Office',
            service_name='Back Office',
            service_desc='Back Office',
            prefix='B',
            display_dashboard_ind=0,
            actual_service_ind=0
        )
        category_exams = theq.Service(
            service_code='Exams',
            service_name='Exams',
            service_desc='Exams',
            prefix='E',
            display_dashboard_ind=0,
            actual_service_ind=0
        )
        db.session.add(category_msp)
        db.session.add(category_ptax)
        db.session.add(category_back_office)
        db.session.add(category_exams)
        db.session.commit()

        # -- Services --------------------------------------------------
        logging.info('--> Services')
        service_msp6 = theq.Service(
            service_code='MSP - 006',
            service_name='Payment - MSP',
            service_desc='MSP- SC686, SC1089 -Pay direct payment, employer '
            'payment',
            parent_id=category_msp.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1,
            external_service_name='Medical Services Plan Payment'
        )
        service_ptax4 = theq.Service(
            service_code='PTAX - 004',
            service_name='Other - PTAX',
            service_desc='PTax/RPT - Providing information, forms, searches, '
            'tax clearance certificate, address changes, add new owner, '
            'extensions, forfeiture status, tax search, etc.',
            parent_id=category_ptax.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1
        )
        service_ptax1 = theq.Service(
            service_code='PTAX - 001',
            service_name='Deferment Application',
            service_desc='PTax/RPT - Process application - new and renewal, '
            'post note, etc.',
            parent_id=category_ptax.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1,
            external_service_name='Rural Property Tax - Deferment Application'
        )
        service_ptax2 = theq.Service(
            service_code='PTAX - 002',
            service_name='Deferment Payment',
            service_desc='PTax/RPT - Full or Partial deferment account '
            'payment',
            parent_id=category_ptax.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1,
            external_service_name='Rural Property Tax - Deferment Payment'
        )
        service_msp1 = theq.Service(
            service_code='MSP - 001',
            service_name='Account Enquiry/Update',
            service_desc='MSP-Address or family changes, personal information '
            'updates, general status enquiries, billing information from '
            'Biller Direct, immigration documents to HIBC, needs PHN, etc.',
            parent_id=category_msp.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1,
            external_service_name='Medical Services Plan Account Update'
        )
        service_msp2 = theq.Service(
            service_code='MSP - 002',
            service_name='BCSC Non Photo',
            service_desc='MSP- SC2607 RAPID ordering, status enquiry, address '
            'update, also for the non photo form process when photo eligible, '
            'etc.',
            parent_id=category_msp.service_id,
            prefix='A',
            display_dashboard_ind=1,
            actual_service_ind=1,
            external_service_name='BC Services Card - Non-photo Card'
        )
        service_bo1 = theq.Service(
            service_code='Back Office - 001',
            service_name='Batching',
            service_desc='Batching',
            parent_id=category_back_office.service_id,
            prefix='B',
            display_dashboard_ind=0,
            actual_service_ind=1
        )
        service_bo2 = theq.Service(
            service_code='Back Office - 002',
            service_name='Cash Out',
            service_desc='Cash Out',
            parent_id=category_back_office.service_id,
            prefix='B',
            display_dashboard_ind=0,
            actual_service_ind=1
        )
        service_exams = theq.Service(
            service_code='Exams - 001',
            service_name='Exam Management',
            service_desc='ITA or PEST -Checking for expired Exams, contacting '
            'ITA or PEST program, mailing back ITA or shredding expired PEST '
            'Exams, etc.',
            parent_id=category_exams.service_id,
            prefix='E',
            display_dashboard_ind=1,
            actual_service_ind=1
        )
        db.session.add(service_bo1)
        db.session.add(service_bo2)
        db.session.add(service_msp1)
        db.session.add(service_msp2)
        db.session.add(service_msp6)
        db.session.add(service_ptax1)
        db.session.add(service_ptax2)
        db.session.add(service_ptax4)
        db.session.add(service_exams)
        db.session.commit()

        # -- Counters --------------------------------------------------
        logging.info('--> Counters')
        qt_counter = theq.Counter(
            counter_name='Quick Trans',
            counter_id=1,
        )
        counter = theq.Counter(
            counter_name='Counter',
            counter_id=2
        )
        db.session.add(qt_counter)
        db.session.add(counter)
        db.session.commit()

        # -- Timezones -------------------------------------------------
        logging.info('--> Timezones')
        timezone_one = theq.Timezone(timezone_name='America/Vancouver')
        timezone_two = theq.Timezone(timezone_name='America/Dawson_Creek')
        timezone_three = theq.Timezone(timezone_name='America/Edmonton')
        timezone_four = theq.Timezone(timezone_name='America/Creston')
        db.session.add(timezone_one)
        db.session.add(timezone_two)
        db.session.add(timezone_three)
        db.session.add(timezone_four)
        db.session.commit()

        # -- Offices ---------------------------------------------------
        logging.info('--> Offices')
        office_test = theq.Office(
            office_name='Test Office',
            office_number=999,
            sb_id=smartboard_call_ticket.sb_id,
            exams_enabled_ind=1,
            timezone_id=timezone_one.timezone_id,
            appointments_enabled_ind=1,
            latitude=48.458359,
            longitude=-123.377106,
            office_appointment_message='Test Message',
            appointments_days_limit=30,
            appointment_duration=30,
            max_person_appointment_per_day=10,
            civic_address='4000 Seymour',
            telephone='999-999-9999',
            online_status='SHOW'
        )
        office_test.counters.append(counter)
        office_test.counters.append(qt_counter)

        office_100 = theq.Office(
            office_name='100 Mile House',
            office_number=1,
            sb_id=smartboard_no_call.sb_id,
            exams_enabled_ind=0,
            timezone_id=timezone_four.timezone_id,
            appointments_enabled_ind=1,
            latitude=51.644,
            longitude=-121.295,
            appointments_days_limit=30,
            appointment_duration=30,
            max_person_appointment_per_day=1,
            civic_address='100 Mile House, BC',
            telephone='999-999-9999',
            online_status='SHOW'
        )
        office_100.counters.append(counter)
        office_100.counters.append(qt_counter)

        office_victoria = theq.Office(
            office_name='Victoria',
            office_number=61,
            sb_id=smartboard_call_name.sb_id,
            exams_enabled_ind=0,
            timezone_id=timezone_one.timezone_id,
            appointments_enabled_ind=1,
            latitude=51.644,
            longitude=-121.295,
            appointments_days_limit=30,
            appointment_duration=30,
            max_person_appointment_per_day=1,
            civic_address='Victoria, BC',
            telephone='999-999-9999',
            online_status='SHOW'
        )
        office_victoria.counters.append(counter)
        office_victoria.counters.append(qt_counter)

        office_pesticide_office = theq.Office(
            office_name='Pesticide Offsite',
            office_number=997,
            sb_id=smartboard_call_name.sb_id,
            exams_enabled_ind=1,
            timezone_id=timezone_one.timezone_id,
            appointments_enabled_ind=0,
            appointments_days_limit=30,
            appointment_duration=30,
            max_person_appointment_per_day=1,
            online_status='HIDE'
        )
        office_pesticide_office.counters.append(counter)
        office_pesticide_office.counters.append(qt_counter)

        db.session.add(office_test)
        db.session.add(office_100)
        db.session.add(office_victoria)
        db.session.add(office_pesticide_office)
        db.session.commit()

        # -- Time Slots ------------------------------------------------
        logging.info('--> Time Slots')
        db.session.add(theq.TimeSlot(
            start_time='08:30:00-07:00',
            end_time='09:30:00-07:00',
            no_of_slots=2,
            day_of_week=['Monday', 'Wednesday'],
            office_id=office_victoria.office_id
        ))
        db.session.add(theq.TimeSlot(
            start_time='09:30:00-07:00',
            end_time='10:30:00-07:00',
            no_of_slots=2,
            day_of_week=['Tuesday'],
            office_id=office_victoria.office_id
        ))
        db.session.add(theq.TimeSlot(
            start_time='13:30:00-07:00',
            end_time='14:30:00-07:00',
            no_of_slots=2,
            day_of_week=['Tuesday', 'Wednesday', 'Thursday'],
            office_id=office_victoria.office_id
        ))
        db.session.commit()

        # -- CSRs ------------------------------------------------------
        logging.info('--> CSRs')
        db.session.add(theq.CSR(
            username='cfms-postman-operator',
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            counter_id=qt_counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=0,
            pesticide_designate=0,
            finance_designate=0,
            ita2_designate=0
        ))
        db.session.add(theq.CSR(
            username='cfms-postman-non-operator',
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            counter_id=counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=0,
            pesticide_designate=0,
            finance_designate=0,
            ita2_designate=0
        ))
        db.session.add(theq.CSR(
            username='demoga',
            office_id=office_test.office_id,
            role_id=role_ga.role_id,
            counter_id=counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=1,
            pesticide_designate=1,
            finance_designate=1,
            ita2_designate=1
        ))
        db.session.add(theq.CSR(
            username='democsr',
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            counter_id=counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=0,
            pesticide_designate=0,
            finance_designate=0,
            ita2_designate=0
        ))
        db.session.add(theq.CSR(
            username='admin',
            office_id=office_test.office_id,
            role_id=role4.role_id,
            counter_id=counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=1,
            pesticide_designate=1,
            finance_designate=1,
            ita2_designate=1
        ))
        db.session.add(theq.CSR(
            username='user',
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            counter_id=counter.counter_id,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id,
            office_manager=0,
            pesticide_designate=0,
            finance_designate=0,
            ita2_designate=0
        ))
        db.session.commit()

        # -- Office Services -------------------------------------------
        logging.info('--> Office Services')
        office_test.services.append(category_back_office)
        office_test.services.append(category_msp)
        office_test.services.append(category_ptax)
        office_test.services.append(category_exams)
        office_test.services.append(service_bo1)
        office_test.services.append(service_bo2)
        office_test.services.append(service_msp1)
        office_test.services.append(service_msp2)
        office_test.services.append(service_msp6)
        office_test.services.append(service_ptax1)
        office_test.services.append(service_ptax2)
        office_test.services.append(service_ptax4)
        office_test.services.append(service_exams)

        office_victoria.services.append(category_back_office)
        office_victoria.services.append(category_msp)
        office_victoria.services.append(service_bo1)
        office_victoria.services.append(service_bo2)
        office_victoria.services.append(service_msp1)
        office_victoria.services.append(service_msp2)
        office_victoria.services.append(service_msp6)

        office_100.services.append(category_back_office)
        office_100.services.append(category_ptax)
        office_100.services.append(service_bo1)
        office_100.services.append(service_bo2)
        office_100.services.append(service_ptax1)
        office_100.services.append(service_ptax2)
        office_100.services.append(service_ptax4)
        db.session.commit()

        # -- Booking / Rooms -------------------------------------------
        logging.info('--> Booking: Rooms')
        db.session.add(bookings.Room(
            office_id=office_test.office_id,
            room_name='Boardroom 1',
            capacity=25,
            color='#EFD469'
        ))
        db.session.add(bookings.Room(
            office_id=office_test.office_id,
            room_name='Turquoise W-135',
            capacity=25,
            color='#EFD469'
        ))
        db.session.commit()

        # -- Booking / Invigilators ------------------------------------
        logging.info('--> Booking: Invigilators')
        db.session.add(bookings.Invigilator(
            invigilator_name='Homer Simpson',
            office_id=office_test.office_id,
            invigilator_notes='He works in a nuclear power plant.',
            contact_phone='2502084247',
            contact_email='homer.j.simpson@gmail.com',
            contract_number='c-000001',
            contract_expiry_date='2018-11-30'
        ))
        db.session.add(bookings.Invigilator(
            invigilator_name='Lisa Simpson',
            office_id=office_test.office_id,
            invigilator_notes='She plays the sax-a-ma-phone during exams',
            contact_phone='555-555-5555',
            contact_email='lisasimpsonesq@gmail.com',
            contract_number='c-000002',
            contract_expiry_date='2018-12-31'
        ))
        db.session.add(bookings.Invigilator(
            invigilator_name='Bart Simpson',
            office_id=office_test.office_id,
            invigilator_notes='Loves using chalk boards to communicate to '
            'examinees',
            contact_phone='555-555-5555',
            contact_email='bartwuzhere@gmail.com',
            contract_number='c-000003',
            contract_expiry_date='2019-01-31'
        ))
        db.session.add(bookings.Invigilator(
            invigilator_name='Pest 1',
            office_id=office_pesticide_office.office_id,
            invigilator_notes='The first pest invigilator is not a pest',
            contact_phone='555-555-5555',
            contact_email='pest_invigilator_1@gmail.com',
            contract_number='c-000003',
            contract_expiry_date='2019-01-31'
        ))
        db.session.add(bookings.Invigilator(
            invigilator_name='Pest 2',
            office_id=office_pesticide_office.office_id,
            invigilator_notes='The second pest invigilator is a pest',
            contact_phone='555-555-5555',
            contact_email='pest_invigilator_2@gmail.com',
            contract_number='c-000003',
            contract_expiry_date='2019-01-31'
        ))
        db.session.commit()

        # -- Booking / Exam Types --------------------------------------
        logging.info('--> Booking: Exam Types')
        db.session.add(bookings.ExamType(
            exam_type_name='COFQ - 3HR Group Exam',
            exam_color='#FF69B4',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=1,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='COFQ - 3HR Single Exam',
            exam_color='#FF69B4',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='COFQ - 3HR Single Exam - Own Reader',
            exam_color='#FF69B4',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='COFQ - 3HR Single Exam - SBC Reader',
            exam_color='#FF69B4',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='COFQ - 3HR Single Exam - Time Extension',
            exam_color='#FF69B4',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='IPSE - 4HR Group Exam',
            exam_color='#FFD701',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=1,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='IPSE - 4HR Single Exam',
            exam_color='#FFD701',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='IPSE - 4HR Single Exam - Own Reader',
            exam_color='#FFD701',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='IPSE - 4HR Single Exam - SBC Reader',
            exam_color='#FFD701',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='IPSE - 4HR Single Exam - Time Extension',
            exam_color='#FFD701',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='SLE - 3HR Group Exam',
            exam_color='#8FBC8F',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=1,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='SLE - 3HR Single Exam',
            exam_color='#8FBC8F',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='SLE - 3HR Single Exam - Own Reader',
            exam_color='#8FBC8F',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='SLE - 3HR Single Exam - SBC Reader',
            exam_color='#8FBC8F',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='SLE - 3HR Single Exam - Time Extension',
            exam_color='#8FBC8F',
            number_of_hours=3,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Monthly Session Exam',
            exam_color='#FFFFFF',
            number_of_hours=4,
            method_type='Written',
            ita_ind=1,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Veterinary Exam',
            exam_color='#FFFFFF',
            number_of_hours=2,
            method_type='written',
            ita_ind=0,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Milk Grader',
            exam_color='#FFFFFF',
            number_of_hours=2,
            method_type='written',
            ita_ind=0,
            group_exam_ind=0,
            pesticide_exam_ind=0
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Industrial Vegetation',
            exam_color='#FFFFFF',
            number_of_hours=3,
            method_type='written',
            ita_ind=0,
            group_exam_ind=0,
            pesticide_exam_ind=1
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Structural-General',
            exam_color='#FFFFFF',
            number_of_hours=3,
            method_type='written',
            ita_ind=0,
            group_exam_ind=0,
            pesticide_exam_ind=1
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Dispenser-Commercial',
            exam_color='#FFFFFF',
            number_of_hours=1,
            method_type='written',
            ita_ind=0,
            group_exam_ind=0,
            pesticide_exam_ind=1
        ))
        db.session.add(bookings.ExamType(
            exam_type_name='Group Environment Exam',
            exam_color='#FFFFFF',
            number_of_hours=0,
            method_type='written',
            ita_ind=0,
            group_exam_ind=1,
            pesticide_exam_ind=0
        ))
        db.session.commit()

        logging.info('--> Booking: Exams - No exams added')
        logging.info('--> Booking: Appointments - No appointments added')


class MigrateWrapper(Command):
    '''
    Wraps flask_migrate's upgrade command to upgrade the database with
    any changes that have been made.
    '''

    def run(self):
        '''
        Runs flask_migrate.upgrade()
        '''
        logging.info('MigrateWrapper.run()') # Show if pods call it.
        upgrade()


manager.add_command('db', MigrateCommand)
manager.add_command('migrate', MigrateWrapper())
manager.add_command('bootstrap', Bootstrap())


if __name__ == '__main__':
    logging.info('Running the Manager')
    manager.run()
