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
        db.session.commit()

        print("Starting to bootstrap data")

        office1 = models.Office("Summerland")
        office2 = models.Office("Test Office")

        db.session.add(office1)
        db.session.add(office2)
        db.session.flush()

        adamkroon = models.User("adamkroon", office1.id)
        cdmcinto = models.User("cdmcinto", office1.id)
        kgillani = models.User("kgillani", office1.id)
        scottrumsby = models.User("scottrumsby", office1.id)
        seanrumsby = models.User("seanrumsby", office1.id)

        cfms_postman_operator = models.User("cfms-postman-operator", office2.id)
        cfms_postman_non_operator = models.User("cfms-postman-non-operator", office2.id)

        db.session.add(adamkroon)
        db.session.add(cdmcinto)
        db.session.add(kgillani)
        db.session.add(scottrumsby)
        db.session.add(seanrumsby)
        db.session.add(cfms_postman_operator)
        db.session.add(cfms_postman_non_operator)

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
