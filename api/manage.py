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

        office1 = models.Office("Vancouver")
        office2 = models.Office("Prince George")
        office3 = models.Office("Vernon")
        office4 = models.Office("Kamloops")
        office5 = models.Office("Kelowna")
        office6 = models.Office("Victoria")
        office7 = models.Office("Port Alberni")
        office8 = models.Office("Summerland")
        office9 = models.Office("Kitimat")

        db.session.add(office1)
        db.session.add(office2)
        db.session.add(office3)
        db.session.add(office4)
        db.session.add(office5)
        db.session.add(office6)
        db.session.add(office7)
        db.session.add(office8)
        db.session.add(office9)

        db.session.flush()

        vancouver_user1 = models.User("vancouver1", "vancouver1", office1.id)
        vancouver_user2 = models.User("vancouver2", "vancouver2", office1.id)
        vancouver_user3 = models.User("vancouver3", "vancouver3", office1.id)

        prince_george_user1 = models.User("princegeorge1", "princegeorge1", office2.id)
        prince_george_user2 = models.User("princegeorge2", "princegeorge2", office2.id)
        prince_george_user3 = models.User("princegeorge3", "princegeorge3", office2.id)

        vernon_user1 = models.User("vernon1", "vernon1", office3.id)
        vernon_user2 = models.User("vernon2", "vernon2", office3.id)
        vernon_user3 = models.User("vernon3", "vernon3", office3.id)

        kamloops1 = models.User("kamloops1", "kamloops1", office4.id)
        kamloops2 = models.User("kamloops2", "kamloops2", office4.id)
        kamloops3 = models.User("kamloops3", "kamloops3", office4.id)

        kelowna1 = models.User("kelowna1", "kelowna1", office5.id)
        kelowna2 = models.User("kelowna2", "kelowna2", office5.id)
        kelowna3 = models.User("kelowna3", "kelowna3", office5.id)

        victoria1 = models.User("victoria1", "victoria1", office6.id)
        victoria2 = models.User("victoria2", "victoria2", office6.id)
        victoria3 = models.User("victoria3", "victoria3", office6.id)

        port_alberni1 = models.User("port_alberni1", "port_alberni1", office7.id)
        port_alberni2 = models.User("port_alberni2", "port_alberni2", office7.id)
        port_alberni3 = models.User("port_alberni3", "port_alberni3", office7.id)

        summerland1 = models.User("summerland1", "summerland1", office8.id)
        summerland2 = models.User("summerland2", "summerland2", office8.id)
        summerland3 = models.User("summerland3", "summerland3", office8.id)

        kitimat1 = models.User("kitimat1", "kitimat1", office9.id)
        kitimat2 = models.User("kitimat2", "kitimat2", office9.id)
        kitimat3 = models.User("kitimat3", "kitimat3", office9.id)

        db.session.add(vancouver_user1)
        db.session.add(vancouver_user2)
        db.session.add(vancouver_user3)

        db.session.add(prince_george_user1)
        db.session.add(prince_george_user2)
        db.session.add(prince_george_user3)

        db.session.add(vernon_user1)
        db.session.add(vernon_user2)
        db.session.add(vernon_user3)

        db.session.add(kamloops1)
        db.session.add(kamloops2)
        db.session.add(kamloops3)

        db.session.add(kelowna1)
        db.session.add(kelowna2)
        db.session.add(kelowna3)

        db.session.add(victoria1)
        db.session.add(victoria2)
        db.session.add(victoria3)

        db.session.add(port_alberni1)
        db.session.add(port_alberni2)
        db.session.add(port_alberni3)

        db.session.add(summerland1)
        db.session.add(summerland2)
        db.session.add(summerland3)

        db.session.add(kitimat1)
        db.session.add(kitimat2)
        db.session.add(kitimat3)

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
