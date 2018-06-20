from flask_restplus import fields
from qsystem import api, db
from .base import Base
from sqlalchemy import BigInteger, Integer, String, DateTime

class Office(Base):

    office_service = db.Table('office_service',
                     db.Column('office_id', db.Integer, 
                                db.ForeignKey('office.office_id', ondelete="CASCADE"), primary_key=True),
                     db.Column('service_id', db.Integer,
                                db.ForeignKey('service.service_id', ondelete="CASCADE"), primary_key=True)
    )

    model = api.model('Office', {
        'office_id': fields.Integer,
        'office_name': fields.String,
        'office_number': fields.Integer,
        'sb_id': fields.Integer,
        'deleted': fields.String
    })

    office_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    office_name     = db.Column(db.String(100))
    office_number   = db.Column(db.Integer)
    sb_id           = db.Column(db.Integer, db.ForeignKey('smartboard.sb_id'))
    deleted         = db.Column(db.DateTime, nullable=True)

    services        = db.relationship("Service", secondary=office_service, back_populates="offices")
    offices         = db.relationship('CSR', backref='office', lazy=False)
    citizens        = db.relationship('Citizen', backref='office', lazy=False)

    def __repr__(self, office_name):
        return '<Office: %r>' % self.office_name

    def __init__(self, office_name, office_number, sb_id):
        self.office_name    = office_name
        self.office_number  = office_number
        self.sb_id          = sb_id

    def json(self, office_id, office_name, office_number, sb_id, deleted):
        return {"office_id" : self.office_id, 
                "office_name" : self.office_name, 
                "office_number" : self.office_number,
                "sb_id" : self.sb_id, 
                "deleted" : self.deleted }