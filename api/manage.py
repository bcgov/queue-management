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
        models.Office.query.delete()
        models.SmartBoard.query.delete()
        models.Citizen.query.delete()
        models.CitizenState.query.delete()
        db.session.commit()

        print("Starting to bootstrap data")

        smartboard1 = models.SmartBoard("Test")

        db.session.add(smartboard1)
        db.session.flush()

        office1 = models.Office("Summerland", 1, smartboard1.sb_id)

        office2 = models.Office("Test Office", 2, smartboard1.sb_id)

        db.session.add(office1)
        db.session.add(office2)
        db.session.flush()

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
