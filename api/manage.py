"""Manage the database and some other items required to run the API"""
from flask_script import Command, Manager, Option # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand, upgrade
from qsystem import db, application
from app import models
import logging
from datetime import datetime

migrate = Migrate(application, db)
manager = Manager(application)

class Bootstrap(Command):

    def run(self):
        print("Clearing out all models")
        models.Period.query.delete()
        models.PeriodState.query.delete()
        models.ServiceReq.query.delete()
        models.SRState.query.delete()
        models.Citizen.query.delete()
        models.CitizenState.query.delete()
        models.CSR.query.delete()
        models.CSRState.query.delete()
        # models.OfficeService.query.delete()   #  This needs to be updated.
        models.Office.query.delete()
        models.SmartBoard.query.delete()
        # models.RolePermission.query.delete()  #  No data in this table yet.
        models.Role.query.delete()
        # models.Permission.query.delete()      #  No data in this table yet.
        models.Service.query.filter_by(actual_service_ind=1).delete()
        models.Service.query.delete()
        models.Channel.query.delete()
        db.session.commit()

        print("Starting to bootstrap data")
        #-- Channels --------------------------------------------------------
        print("--> Channels")
        channel1 = models.Channel(
            channel_name="In Person"
        )
        channel2 = models.Channel(
            channel_name="Phone"
        )
        channel3 = models.Channel(
            channel_name="Back Office"
        )
        channel4 = models.Channel(
            channel_name="Email/Fax/Mail"
        )
        channel5 = models.Channel(
            channel_name="CATs Assist"
        )
        channel6 = models.Channel(
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
        role_csr = models.Role(
            role_code="CSR",
            role_desc="Customer Service Representative"
        )
        role_ga = models.Role(
            role_code="GA",
            role_desc="Government Agent"
        )
        role3 = models.Role(
            role_code="HELPDESK",
            role_desc="Help Desk Functions"
        )
        role4 = models.Role(
            role_code="SUPPORT",
            role_desc="All Administrative Functions"
        )
        role5 = models.Role(
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
        period_state1 = models.PeriodState(
            ps_name="Waiting",
            ps_desc="Waiting in line to see a CSR, after a ticket has been created for them. The time they are in this state is the Citizen Wait Time",
            ps_number=1
        )
        period_state2 = models.PeriodState(
            ps_name="Ticket Creation",
            ps_desc="A receptionist is creating a service request / ticket for the citizen. This is the first state a citizen will be in. The time they are in this state is the CSR prep time.",
            ps_number=2
        )
        period_state3 = models.PeriodState(
            ps_name="Invited",
            ps_desc="Has been called from the waiting area to be served. The time they are in this state is the time it takes them to walk from the waiting area, to the CSR, until the CSR starts to serve them.",
            ps_number=4
        )
        period_state4 = models.PeriodState(
            ps_name="Being Served",
            ps_desc="Is being servbed by a CSR. The time they are in this state is the Service time.",
            ps_number=7
        )
        period_state5 = models.PeriodState(
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
        smartboard_call_name = models.SmartBoard(sb_type="callbyname")
        smartboard_call_ticket = models.SmartBoard(sb_type="callbyticket")
        smartboard_no_call = models.SmartBoard(sb_type="nocallonsmartboard")
        db.session.add(smartboard_call_name)
        db.session.add(smartboard_call_ticket)
        db.session.add(smartboard_no_call)
        db.session.commit()

        #-- Citizen state values --------------------------------------------
        print("--> Citizen State")
        cs1 = models.CitizenState(
            cs_state_name="Active",
            cs_state_desc="Citizen is active, a ticket is being or has been created for them"
        )
        cs2 = models.CitizenState(
            cs_state_name="Received Services",
            cs_state_desc="Citizen left after receiving services"
        )
        cs3 = models.CitizenState(
            cs_state_name="Left before receiving services",
            cs_state_desc="Citizen left, after ticket creation, before service was started for them"
        )
        db.session.add(cs1)
        db.session.add(cs2)
        db.session.add(cs3)
        db.session.commit()

        #-- CSR state values     --------------------------------------------
        print("--> CSR State")
        csr_state_logout = models.CSRState(
            csr_state_name="Logout",
            csr_state_desc="Logged out"
        )
        csr_state2 = models.CSRState(
            csr_state_name="Login",
            csr_state_desc="Logged in"
        )
        csr_state3 = models.CSRState(
            csr_state_name="Break",
            csr_state_desc="Currently on break"
        )
        csr_state4 = models.CSRState(
            csr_state_name="Serving",
            csr_state_desc="Serving a citizen"
        )
        csr_state5 = models.CSRState(
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
        sr_state1 = models.SRState(
            sr_code="Pending",
            sr_state_desc="Service Request is pending, citizen has not started receiving services yet."
        )
        sr_state2 = models.SRState(
            sr_code="Active",
            sr_state_desc="Service Request is active.  A citizen has started being served."
        )
        sr_state3 = models.SRState(
            sr_code="Complete",
            sr_state_desc="The service has been received for this Service Request."
        )
        db.session.add(sr_state1)
        db.session.add(sr_state2)
        db.session.add(sr_state3)
        db.session.commit()

        #-- Service Category values -----------------------------------------
        print("--> Categories and Services")
        category_msp = models.Service(
            service_code = "MSP",
            service_name = "MSP",
            service_desc = "Medical Services Plan",
            prefix = "A",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )
        category_ptax = models.Service(
            service_code = "PTAX",
            service_name = "Property Tax",
            service_desc = "Property Tax",
            prefix = "A",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )

        category_back_office = models.Service(
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
        service_msp6 = models.Service(
            service_code = "MSP - 006",
            service_name = "Payment - MSP",
            service_desc = "MSP- SC686, SC1089 -Pay direct payment, employer payment",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax4 = models.Service(
            service_code = "PTAX - 004",
            service_name = "Other - PTAX",
            service_desc = "PTax/RPT - Providing information, forms, searches, tax clearance certificate, address changes, add new owner, extensions, forfeiture status, tax search, etc.",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax1 = models.Service(
            service_code = "PTAX - 001",
            service_name = "Deferment Application",
            service_desc = "PTax/RPT - Process application - new and renewal, post note, etc.",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_ptax2 = models.Service(
            service_code = "PTAX - 002",
            service_name = "Deferment Payment",
            service_desc = "PTax/RPT - Full or Partial deferment account payment",
            parent_id = category_ptax.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_msp1 = models.Service(
            service_code = "MSP - 001",
            service_name = "Account Enquiry/Update",
            service_desc = "MSP-Address or family changes, personal information updates, general status enquiries, billing information from Biller Direct, immigration documents to HIBC, needs PHN, etc.",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_msp2 = models.Service(
            service_code = "MSP - 002",
            service_name = "BCSC Non Photo",
            service_desc = "MSP- SC2607 RAPID ordering , status enquiry, address update, also for the non photo form process when photo eligible, etc.",
            parent_id = category_msp.service_id,
            prefix = "A",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_bo1 = models.Service(
            service_code = "Back Office - 001",
            service_name = "Batching",
            service_desc = "Batching",
            parent_id = category_back_office.service_id,
            prefix = "B",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )
        service_bo2 = models.Service(
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
        office_test = models.Office(
            office_name="Test Office",
            office_number=999,
            sb_id=smartboard_call_ticket.sb_id
        )
        office_100 = models.Office(
            office_name="100 Mile House",
            office_number=1,
            sb_id=smartboard_no_call.sb_id
        )
        office_victoria = models.Office(
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
        cfms_postman_operator = models.CSR(
            username="cfms-postman-operator",
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        cfms_postman_non_operator = models.CSR(
            username="cfms-postman-non-operator",
            office_id=office_test.office_id,
            role_id=role_csr.role_id,
            qt_xn_csr_ind=0,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        demo_ga = models.CSR(
            username="demoga",
            office_id=office_test.office_id,
            role_id=role_ga.role_id,
            qt_xn_csr_ind=0,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state_logout.csr_state_id
        )
        demo_csr = models.CSR(
            username="democsr",
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

class FetchData(Command):

    def run(self):
        offices = db.session.query(models.Office).all()
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

        user = models.User(username, password, office_id)
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
