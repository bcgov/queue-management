from flask_restplus import fields
from qsystem import api, db
from base import Base 

class CitizenTable(MyBase, Base, db.model):

    model = api.model ('CitizenTable' {
        'citizen_id' : fields.Integer,
        'office_id' : fields.Integer,
        'ticket_number' : fields.Integer,
        'citizen_name' : fields.String,
        'citizen_comments' : fields.String,
        'qt_xn_citizen' : fields.Integer,
        'cs_id_now' : fields.Integer
        })

    citizen_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # TODO foreign key check to office table
    office_id = db.Column(db.BigInteger)
    # TODO unique value
    ticket_number = db.Column(String(50))
    citizen_name = db.Column(String(150))
    citizen_comments = db.Column(String(1000))
    # TODO find a better way to represent tinyint(1) than Integer
    qt_xn_citizen = db.Column(Integer)
    cs_id_now = db.Column(BigInteger)

    def __repr__(self, citizen_name):
        return '<Citizen: %r>' % self.citizen_name

    # TODO redo init function to include kwargs
    def __init__(self, citizen_id, office_id, ticket_number, citizen_name, citizen_comments, qt_xn_citizen, 
                cs_id_now):
        self.citizen_id = citizen_name
        self.office_id = office_id
        self.ticket_number = ticket_number
        self.citizen_name = citizen_name
        self.citizen_comments = citizen_comments
        self.qt_xn_citizen = qt_xn_citizen
        self.cs_id_now = cs_id_now

    def json(self, citizen_id, office_id, ticket_number, citizen_name, citizen_comments, qt_xn_citizen, 
            cs_id_now):
        return {"citizen_id" : self.citizen_name, "office_id" : self.office_id, "ticket_number" : self.ticket_number,
                "citizen_name" : citizen_name, "citizen_comments" : self.citizen_comments, 
                "qt_xn_citizen" : self.qt_xn_citizen, "cs_id_now" : self.cs_id_now}
