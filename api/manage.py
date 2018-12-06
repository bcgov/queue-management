"""Manage the database and some other items required to run the API"""
from flask_script import Command, Manager, Option # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand, upgrade
from qsystem import db, application
from app.models import theq
from app.models import bookings
import logging
from datetime import datetime

migrate = Migrate(application, db)
manager = Manager(application)

class Bootstrap(Command):

    def run(self):
        print("Clearing out all models")
        theq.Period.query.delete()
        theq.PeriodState.query.delete()
        theq.ServiceReq.query.delete()
        theq.SRState.query.delete()
        theq.Citizen.query.delete()
        theq.CitizenState.query.delete()
        theq.CSR.query.delete()
        theq.CSRState.query.delete()
        # theq.OfficeService.query.delete()   #  This needs to be updated.
        bookings.Exam.query.delete()
        bookings.ExamType.query.delete()
        bookings.Room.query.delete()
        bookings.Invigilator.query.delete()
        theq.Office.query.delete()
        theq.SmartBoard.query.delete()
        # theq.RolePermission.query.delete()  #  No data in this table yet.
        theq.Role.query.delete()
        # theq.Permission.query.delete()      #  No data in this table yet.
        theq.Service.query.filter_by(actual_service_ind=1).delete()
        theq.Service.query.delete()
        theq.Channel.query.delete()
        bookings.Booking.query.delete()

        db.session.commit()

        print("Starting to bootstrap data")
        #-- Channels --------------------------------------------------------
        print("--> Channels")
        channel1 = theq.Channel(
            channel_name="In Person"
        )
        channel2 = theq.Channel(
            channel_name="Phone"
        )
        channel3 = theq.Channel(
            channel_name="Back Office"
        )
        channel4 = theq.Channel(
            channel_name="Email/Fax/Mail"
        )
        channel5 = theq.Channel(
            channel_name="CATs Assist"
        )
        channel6 = theq.Channel(
            channel_name="Mobile Assist"
        )
        db.session.add(channel1)
        db.session.add(channel2)
        db.session.add(channel3)
        db.session.add(channel4)
        db.session.add(channel5)
        db.session.add(channel6)
        db.session.commit()

        #-- Roles -----------------------------------------------------------
        print("--> Roles")
        role_csr = theq.Role(
            role_code="CSR",
            role_desc="Customer Service Representative"
        )
        role_ga = theq.Role(
            role_code="GA",
            role_desc="Government Agent"
        )
        role3 = theq.Role(
            role_code="HELPDESK",
            role_desc="Help Desk Functions"
        )
        role4 = theq.Role(
            role_code="SUPPORT",
            role_desc="All Administrative Functions"
        )
        role5 = theq.Role(
            role_code="ANALYTICS",
            role_desc="Analtyics Team to update Services per Office"
        )
        db.session.add(role_csr)
        db.session.add(role_ga)
        db.session.add(role3)
        db.session.add(role4)
        db.session.add(role5)
        db.session.commit()

        #-- Period State ----------------------------------------------------
        print("--> Period States")
        period_state1 = theq.PeriodState(
            ps_name="Waiting",
            ps_desc="Waiting in line to see a CSR, after a ticket has been created for them. The time they are in this state is the Citizen Wait Time",
            ps_number=1
        )
        period_state2 = theq.PeriodState(
            ps_name="Ticket Creation",
            ps_desc="A receptionist is creating a service request / ticket for the citizen. This is the first state a citizen will be in. The time they are in this state is the CSR prep time.",
            ps_number=2
        )
        period_state3 = theq.PeriodState(
            ps_name="Invited",
            ps_desc="Has been called from the waiting area to be served. The time they are in this state is the time it takes them to walk from the waiting area, to the CSR, until the CSR starts to serve them.",
            ps_number=4
        )
        period_state4 = theq.PeriodState(
            ps_name="Being Served",
            ps_desc="Is being servbed by a CSR. The time they are in this state is the Service time.",
            ps_number=7
        )
        period_state5 = theq.PeriodState(
            ps_name="On hold",
            ps_desc="Has been placed on hold be a csr. The time they are in this state is the Hold time",
            ps_number=11
        )
        db.session.add(period_state1)
        db.session.add(period_state2)
        db.session.add(period_state3)
        db.session.add(period_state4)
        db.session.add(period_state5)
        db.session.commit()

        #-- Smartboard values -----------------------------------------------
        print("--> Smartboard")
        smartboard_call_name = theq.SmartBoard(sb_type="callbyname")
        smartboard_call_ticket = theq.SmartBoard(sb_type="callbyticket")
        smartboard_no_call = theq.SmartBoard(sb_type="nocallonsmartboard")
        db.session.add(smartboard_call_name)
        db.session.add(smartboard_call_ticket)
        db.session.add(smartboard_no_call)
        db.session.commit()

        #-- Citizen state values --------------------------------------------
        print("--> Citizen State")
        cs1 = theq.CitizenState(
            cs_state_name="Active",
            cs_state_desc="Citizen is active, a ticket is being or has been created for them"
        )
        cs2 = theq.CitizenState(
            cs_state_name="Received Services",
            cs_state_desc="Citizen left after receiving services"
        )
        cs3 = theq.CitizenState(
            cs_state_name="Left before receiving services",
            cs_state_desc="Citizen left, after ticket creation, before service was started for them"
        )
        db.session.add(cs1)
        db.session.add(cs2)
        db.session.add(cs3)
        db.session.commit()

        #-- CSR state values     --------------------------------------------
        print("--> CSR State")
        csr_state_logout = theq.CSRState(
            csr_state_name="Logout",
            csr_state_desc="Logged out"
        )
        csr_state2 = theq.CSRState(
            csr_state_name="Login",
            csr_state_desc="Logged in"
        )
        csr_state3 = theq.CSRState(
            csr_state_name="Break",
            csr_state_desc="Currently on break"
        )
        csr_state4 = theq.CSRState(
            csr_state_name="Serving",
            csr_state_desc="Serving a citizen"
        )
        csr_state5 = theq.CSRState(
            csr_state_name="Back Office",
            csr_state_desc="Currently doing back office work"
        )
        db.session.add(csr_state_logout)
        db.session.add(csr_state2)
        db.session.add(csr_state3)
        db.session.add(csr_state4)
        db.session.add(csr_state5)
        db.session.commit()

        #-- Service Request values ------------------------------------------
        print("--> Service Request states")
        sr_state1 = theq.SRState(
            sr_code="Pending",
            sr_state_desc="Service Request is pending, citizen has not started receiving services yet."
        )
        sr_state2 = theq.SRState(
            sr_code="Active",
            sr_state_desc="Service Request is active.  A citizen has started being served."
        )
        sr_state3 = theq.SRState(
            sr_code="Complete",
            sr_state_desc="The service has been received for this Service Request."
        )
        db.session.add(sr_state1)
        db.session.add(sr_state2)
        db.session.add(sr_state3)
        db.session.commit()

        #-- Service Category values -----------------------------------------
        print("--> Categories and Services")
        category_msp = theq.Service(
            service_code = "MSP",
            service_name = "MSP",
            service_desc = "Medical Services Plan",
            prefix = "A",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )
        category_ptax = theq.Service(
            service_code = "PTAX",
            service_name = "Property Tax",
            service_desc = "Property Tax",
            prefix = "A",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )

        category_back_office = theq.Service(
            service_code = "Back Office",
            service_name = "Back Office",
            service_desc = "Back Office",
            prefix = "B",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )
        db.session.add(category_msp)
        db.session.add(category_ptax)
        db.session.add(category_back_office)
        db.session.commit()

        #-- Service values --------------------------------------------------
        service_msp6 = theq.Service(
            service_code = "MSP - 006",
            service_name = "Payment - MSP",
            service_desc = "MSP- SC686, SC1089 -Pay direct payment, employer payment",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax4 = theq.Service(
            service_code = "PTAX - 004",
            service_name = "Other - PTAX",
            service_desc = "PTax/RPT - Providing information, forms, searches, tax clearance certificate, address changes, add new owner, extensions, forfeiture status, tax search, etc.",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax1 = theq.Service(
            service_code = "PTAX - 001",
            service_name = "Deferment Application",
            service_desc = "PTax/RPT - Process application - new and renewal, post note, etc.",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax2 = theq.Service(
            service_code = "PTAX - 002",
            service_name = "Deferment Payment",
            service_desc = "PTax/RPT - Full or Partial deferment account payment",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_msp1 = theq.Service(
            service_code = "MSP - 001",
            service_name = "Account Enquiry/Update",
            service_desc = "MSP-Address or family changes, personal information updates, general status enquiries, billing information from Biller Direct, immigration documents to HIBC, needs PHN, etc.",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_msp2 = theq.Service(
            service_code = "MSP - 002",
            service_name = "BCSC Non Photo",
            service_desc = "MSP- SC2607 RAPID ordering , status enquiry, address update, also for the non photo form process when photo eligible, etc.",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_bo1 = theq.Service(
            service_code = "Back Office - 001",
            service_name = "Batching",
            service_desc = "Batching",
            parent_id = category_back_office.service_id,
            prefix = "B",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_bo2 = theq.Service(
            service_code = "Back Office - 002",
            service_name = "Cash Out",
            service_desc = "Cash Out",
            parent_id = category_back_office.service_id,
            prefix = "B",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        db.session.add(service_bo1)
        db.session.add(service_bo2)
        db.session.add(service_msp1)
        db.session.add(service_msp2)
        db.session.add(service_msp6)
        db.session.add(service_ptax1)
        db.session.add(service_ptax2)
        db.session.add(service_ptax4)
        db.session.commit()

        #-- Office values ---------------------------------------------------
        print("--> Offices")
        office_test = theq.Office(
            office_name="Test Office",
            office_number=999,
            sb_id=smartboard_call_ticket.sb_id
        )
        office_100 = theq.Office(
            office_name="100 Mile House",
            office_number=1,
            sb_id=smartboard_no_call.sb_id
        )
        office_victoria = theq.Office(
            office_name="Victoria",
            office_number=61,
            sb_id=smartboard_call_name.sb_id
        )
        db.session.add(office_test)
        db.session.add(office_100)
        db.session.add(office_victoria)
        db.session.commit()

        #-- CSR values ------------------------------------------------------
        print("--> CSRs")
        cfms_postman_operator = theq.CSR(
            username="cfms-postman-operator",
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        cfms_postman_non_operator = theq.CSR(
            username="cfms-postman-non-operator",
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            qt_xn_csr_ind=0,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        demo_ga = theq.CSR(
            username="admin",
            office_id=office_test.office_id,
            role_id=role_ga.role_id,
            qt_xn_csr_ind=0,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        demo_csr = theq.CSR(
            username="user",
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            qt_xn_csr_ind=0,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        db.session.add(cfms_postman_operator)
        db.session.add(cfms_postman_non_operator)
        db.session.add(demo_ga)
        db.session.add(demo_csr)
        db.session.commit()

        #-- The Office / Services values ------------------------------------
        print("--> Office Services")
        office_test.services.append(category_back_office)
        office_test.services.append(category_msp)
        office_test.services.append(category_ptax)
        office_test.services.append(service_bo1)
        office_test.services.append(service_bo2)
        office_test.services.append(service_msp1)
        office_test.services.append(service_msp2)
        office_test.services.append(service_msp6)
        office_test.services.append(service_ptax1)
        office_test.services.append(service_ptax2)
        office_test.services.append(service_ptax4)

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

        print("--> Bookings: Rooms")
        room_one = bookings.Room(
            office_id = office_test.office_id,
            room_name = "Boardroom 1",
            capacity = 25,
            color = "red"
        )
        room_two = bookings.Room(
            office_id = office_victoria.office_id,
            room_name = "Turquoise W-135",
            capacity = 25,
            color = "red"
        )


        db.session.add(room_one)
        db.session.add(room_two)
        db.session.commit()

        print("--> Bookings: Invigilators")
        invigilator_one = bookings.Invigilator(
            invigilator_name = "Homer Simpson",
            office_id = office_test.office_id,
            invigilator_notes = "He works in a nuclear power plant.",
            contact_phone = "2502084247",
            contact_email = "homer.j.simpson@gmail.com",
            contract_number = "c-000001",
            contract_expiry_date = "2018-11-30"
        )

        invigilator_two = bookings.Invigilator(
            invigilator_name = "Lisa Simpson",
            office_id = office_test.office_id,
            invigilator_notes = "She plays the sax-a-ma-phone during exams",
            contact_phone = "555-555-5555",
            contact_email = "lisasimpsonesq@gmail.com",
            contract_number = "c-000002",
            contract_expiry_date = "2018-12-31"
        )

        invigilator_three = bookings.Invigilator(
            invigilator_name="Bart Simpson",
            office_id=office_test.office_id,
            invigilator_notes="Loves using chalk boards to communicate to examinees",
            contact_phone="555-555-5555",
            contact_email="bartwuzhere@gmail.com",
            contract_number="c-000003",
            contract_expiry_date="2019-01-31"
        )

        db.session.add(invigilator_one)
        db.session.add(invigilator_two)
        db.session.add(invigilator_three)
        db.session.commit()

        print("--> Bookings: Exam Types")
        exam_type_one = bookings.ExamType(
            exam_type_name = "ITA Exam Type",
            exam_color = "red",
            number_of_hours = 3,
            method_type = "Written",
            ita_ind = 1
        )

        exam_type_two = bookings.ExamType(
            exam_type_name = "Pesticide Exam",
            exam_color = "green",
            number_of_hours = 2,
            method_type = "Written",
            ita_ind = 0
        )

        exam_type_three = bookings.ExamType(
            exam_type_name = "Milk Exam",
            exam_color = "white",
            number_of_hours = 1,
            method_type = "Written",
            ita_ind = 0
        )

        db.session.add(exam_type_one)
        db.session.add(exam_type_two)
        db.session.add(exam_type_three)
        db.session.commit()

        print("--> Bookings: Booking")
        booking_one = bookings.Booking(
            room_id = room_one.room_id,
            start_time = "2018-11-29 9:00:00.0",
            end_time = "2018-11-29 12:00:00.0",
            fees = "false",
            booking_name = "Carpentry Exam"
        )

        booking_two = bookings.Booking(
            room_id = room_two.room_id,
            start_time = "2018-11-29 13:00:00.0",
            end_time = "2018-11-29 16:00:00.0",
            fees = "true",
            booking_name = "Plubming Exam"
        )

        booking_three = bookings.Booking(
            room_id = room_one.room_id,
            start_time = "2018-11-29 9:00:00.0",
            end_time = "2018-11-29 12:00:00.0",
            fees = "true",
            booking_name = "Kitchen Exam"
        )

        db.session.add(booking_one)
        db.session.add(booking_two)
        db.session.add(booking_three)
        db.session.commit()

        print("--> Bookings: Exam")
        exam_one = bookings.Exam(
            exam_type_id = exam_type_one.exam_type_id,
            booking_id = booking_one.booking_id,
            invigilator_id = invigilator_one.invigilator_id,
            office_id = office_test.office_id,
            room_id = room_one.room_id,
            event_id = "1234abcd",
            exam_name = "Carpentry Red Seal",
            examinee_name = "Chandler Bing",
            expiry_date = "2018-11-29 11:19:53.5",
            notes = "This student is extremely s-m-r-t",
            exam_received = 1,
            session_number = 1,
            number_of_students = 1,
            exam_method = "Written"
        )

        exam_two = bookings.Exam(
            exam_type_id = exam_type_two.exam_type_id,
            booking_id = booking_two.booking_id,
            invigilator_id = invigilator_two.invigilator_id,
            office_id = office_test.office_id,
            room_id = room_two.room_id,
            event_id = "e-000001",
            exam_name = "Plumbing Red Seal",
            examinee_name = "Joey Fatone",
            expiry_date = "2018-11-29 11:19:53.5",
            notes = "Speak slowly with this student, hearing impaired",
            exam_received = 0,
            session_number = 2,
            number_of_students = 12,
            exam_method = "Written"
        )

        exam_three = bookings.Exam(
            exam_type_id=exam_type_three.exam_type_id,
            booking_id=booking_three.booking_id,
            invigilator_id=invigilator_three.invigilator_id,
            office_id=office_test.office_id,
            room_id=room_two.room_id,
            event_id="e-000002",
            exam_name="Culinary Red Seal",
            examinee_name="Anthony Bourdain",
            expiry_date="2018-11-29 11:19:53.5",
            notes="Student is extremely verbally obscene",
            exam_received=1,
            session_number=3,
            number_of_students=10,
            exam_method="Kitchen"
        )

        db.session.add(exam_one)
        db.session.add(exam_two)
        db.session.add(exam_three)
        db.session.commit()

class FetchData(Command):

    def run(self):
        offices = db.session.query(theq.Office).all()
        for o in offices:
            print(o.id, o.name)

class CreateUser(Command):
    option_list = (
        Option('--username', '-u', dest='username'),
        Option('--password', '-p', dest='password'),
        Option('--office_id', '-o', dest='office_id'),
    )

    def run(self, username, password, office_id):

        if username is None or password is None or office_id is None:
            exit("Error, username, password and office_id are all required")

        user = theq.User(username, password, office_id)
        db.session.add(user)
        db.session.commit()

class MigrateWrapper(Command):
    def run(self):
        upgrade()

manager.add_command('db', MigrateCommand)
manager.add_command('migrate', MigrateWrapper())
manager.add_command('bootstrap', Bootstrap())
manager.add_command('fetch', FetchData())
manager.add_command('create_user', CreateUser())

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()