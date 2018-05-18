"""Manage the database and some other items required to run the API"""
from flask_script import Command, Manager, Option # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
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

        office1 = models.Office("Vancouver")
        office2 = models.Office("Prince George")
        office3 = models.Office("Vernon")

        db.session.add(office1)
        db.session.add(office2)
        db.session.add(office3)

        db.session.flush()

        vancouverUser1 = models.User("vancouver1", "vancouver1", office1.id)
        vancouverUser2 = models.User("vancouver2", "vancouver2", office1.id)
        vancouverUser3 = models.User("vancouver3", "vancouver3", office1.id)

        princeGeorgeUser1 = models.User("princegeorge1", "princegeorge1", office2.id)
        princeGeorgeUser2 = models.User("princegeorge2", "princegeorge2", office2.id)
        princeGeorgeUser3 = models.User("princegeorge3", "princegeorge3", office2.id)

        vernonUser1 = models.User("vernon1", "vernon1", office3.id)
        vernonUser2 = models.User("vernon2", "vernon2", office3.id)
        vernonUser3 = models.User("vernon3", "vernon3", office3.id)


        db.session.add(vancouverUser1)
        db.session.add(vancouverUser2)
        db.session.add(vancouverUser3)

        db.session.add(princeGeorgeUser1)
        db.session.add(princeGeorgeUser2)
        db.session.add(princeGeorgeUser3)

        db.session.add(vernonUser1)
        db.session.add(vernonUser2)
        db.session.add(vernonUser3)

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

manager.add_command('db', MigrateCommand)
manager.add_command('bootstrap', Bootstrap())
manager.add_command('fetch', FetchData())
manager.add_command('create_user', CreateUser())

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()
