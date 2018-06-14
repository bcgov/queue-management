from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String

class Citizen(Base):

    model = api.model('Citizen', {
        'citizen_id' : fields.Integer,
        'office_id' : fields.Integer,
        'ticket_number' : fields.Integer,
        'citizen_name' : fields.String,
        'citizen_comments' : fields.String,
        'qt_xn_citizen' : fields.Integer,
        'cs_id_now' : fields.Integer
        })

    citizen_id          = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    office_id           = db.Column(db.BigInteger, db.ForeignKey('office.office_id'))
    ticket_number       = db.Column(String(50))
    citizen_name        = db.Column(String(150))
    citizen_comments    = db.Column(String(1000))
    qt_xn_citizen       = db.Column(Integer)
    # TODO - CFMS Data Dictionary says that cs_id_now exists on citizen state table, 
    # however it does not. Please review.
    cs_id_now           = db.Column(BigInteger)

    office = db.relationship('Office')

    def __repr__(self, citizen_name):
        return '<Citizen: %r>' % self.citizen_name

    args = {'citizen_id': 'citizen_id',
            'office_id': 'office_id',
            'ticket_number': 'ticket_number',
            'citizen_name': 'citizen_name',
            'citizen_comments': 'citizen_comments',
            'qt_xn_citizen': 'qt_xn_citizen',
            'cs_id_now': 'cs_id_now'}

    # TODO redo init function to include kwargs
    def __init__(self, **args):
        self.citizen_id         = args['citizen_name']
        self.office_id          = args['office_id']
        self.ticket_number      = args['ticket_number']
        self.citizen_name       = args['citizen_name']
        self.citizen_comments   = args['citizen_comments']
        self.qt_xn_citizen      = args['qt_xn_citizen']
        self.cs_id_now          = args['cs_id_now']

    json_args = {"citizen_id" : self.citizen_name, 
                "office_id" : self.office_id, 
                "ticket_number" : self.ticket_number,
                "citizen_name" : citizen_name, 
                "citizen_comments" : self.citizen_comments, 
                "qt_xn_citizen" : self.qt_xn_citizen, 
                "cs_id_now" : self.cs_id_now}

    def json(self, json_args):
        return json_args
