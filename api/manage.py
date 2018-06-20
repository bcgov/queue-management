"""Manage the database and some other items required to run the API"""
from flask_script import Command, Manager, Option # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand, upgrade
from qsystem import db, application
from app import models
import logging

migrate = Migrate(application, db)
manager = Manager(application)

class Bootstrap(Command):

    def run(self):
        print("Clearing out all models")
        models.Client.query.delete()
        models.User.query.delete()
        models.Citizen.query.delete()
        models.CitizenState.query.delete()
        models.Channel.query.delete()
        models.Service.query.filter_by(actual_service=1).delete()
        models.Service.query.delete()
        models.Office.query.delete()
        models.SmartBoard.query.delete()
        db.session.commit()

        print("Starting to bootstrap data")

        smartboard1 = models.SmartBoard("Test")

        db.session.add(smartboard1)
        db.session.flush()

        office1 = models.Office("Summerland", 1, smartboard1.sb_id)

        office2 = models.Office("Victoria", 2, smartboard1.sb_id)

        office3 = models.Office("Vernon", 3, smartboard1.sb_id)

        office4 = models.Office("Test Office", 4, smartboard1.sb_id)

        db.session.add(office1)
        db.session.add(office2)
        db.session.add(office3)
        db.session.add(office4)
        db.session.flush()

        category1 = models.Service(
            service_name = "Licenses",
            actual_service = 0
        )

        category2 = models.Service(
            service_name = "Taxes",
            actual_service = 0
        )

        category3 = models.Service(
            service_name = "ICBC",
            actual_service = 0
        )

        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.flush()

        service1 = models.Service(
            service_name = "Fishing",
            parent_id = category1.service_id,
            actual_service = 1
        )

        service2 = models.Service(
            service_name = "Hunting",
            parent_id = category1.service_id,
            actual_service = 1
        )

        service3 = models.Service(
            service_name = "Gold Mining",
            parent_id = category1.service_id,
            actual_service = 1
        )

        service4 = models.Service(
            service_name = "Property Taxes",
            parent_id = category2.service_id,
            actual_service = 1
        )

        service5 = models.Service(
            service_name = "MSP",
            parent_id = category2.service_id,
            actual_service = 1
        )

        service6 = models.Service(
            service_name = "Class 5 Test",
            parent_id = category3.service_id,
            actual_service = 1
        )

        service7 = models.Service(
            service_name = "Speeding Ticket",
            parent_id = category3.service_id,
            actual_service = 1
        )

        service8 = models.Service(
            service_name = "Class 6 Test",
            parent_id = category3.service_id,
            actual_service = 1
        )

        service9 = models.Service(
            service_name = "DUI",
            parent_id = category3.service_id,
            actual_service = 1
        )

        db.session.add(service1)
        db.session.add(service2)
        db.session.add(service3)
        db.session.add(service4)
        db.session.add(service5)
        db.session.add(service6)
        db.session.add(service7)
        db.session.add(service8)
        db.session.add(service9)
        db.session.commit()

        office1.services.append(category1)
        office1.services.append(category2)
        office1.services.append(category3)
        office1.services.append(service1)
        office1.services.append(service2)
        office1.services.append(service3)
        office1.services.append(service4)
        office1.services.append(service5)
        office1.services.append(service6)
        office1.services.append(service7)
        office1.services.append(service8)
        office1.services.append(service9)

        office2.services.append(category2)
        office2.services.append(category3)
        office2.services.append(service4)
        office2.services.append(service5)
        office2.services.append(service6)
        office2.services.append(service7)
        office2.services.append(service8)
        office2.services.append(service9)

        office3.services.append(category1)
        office3.services.append(category2)
        office3.services.append(service1)
        office3.services.append(service2)
        office3.services.append(service3)
        office3.services.append(service4)
        office3.services.append(service5)

        office4.services.append(category1)
        office4.services.append(category2)
        office4.services.append(category3)
        office4.services.append(service1)
        office4.services.append(service2)
        office4.services.append(service3)
        office4.services.append(service4)
        office4.services.append(service5)
        office4.services.append(service6)
        office4.services.append(service7)
        office4.services.append(service8)
        office4.services.append(service9)

        adamkroon = models.User("adamkroon", office1.office_id)
        cdmcinto = models.User("cdmcinto", office1.office_id)
        kgillani = models.User("kgillani", office1.office_id)
        scottrumsby = models.User("scottrumsby", office1.office_id)
        seanrumsby = models.User("seanrumsby", office1.office_id)

        cfms_postman_operator = models.User("cfms-postman-operator", office2.office_id)
        cfms_postman_non_operator = models.User("cfms-postman-non-operator", office2.office_id)

        db.session.add(adamkroon)
        db.session.add(cdmcinto)
        db.session.add(kgillani)
        db.session.add(scottrumsby)
        db.session.add(seanrumsby)
        db.session.add(cfms_postman_operator)
        db.session.add(cfms_postman_non_operator)

        db.session.commit()

        cs1 = models.CitizenState(
            cs_state_name="Test",
            cs_state_desc="Blah"
        )

        db.session.add(cs1)
        db.session.flush()

        john = models.Citizen(
        office_id = office1.office_id,
        ticket_number = "1",
        citizen_name = "John",
        citizen_comments = "Blorp",
        qt_xn_citizen = 0,
        cs_id = cs1.cs_id
        )

        db.session.add(john)
        db.session.commit()

        channel1 = models.Channel("In Person")
        channel2 = models.Channel("Telephone")
        channel3 = models.Channel("Email")

        db.session.add(channel1)
        db.session.add(channel2)
        db.session.add(channel3)
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
