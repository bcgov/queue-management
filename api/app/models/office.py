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

    office_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    office_name     = db.Column(db.String(100))
    office_number   = db.Column(db.Integer)
    sb_id           = db.Column(db.Integer, db.ForeignKey('smartboard.sb_id'))
    deleted         = db.Column(db.DateTime, nullable=True)

    services        = db.relationship("Service", secondary=office_service, back_populates="offices")
    csrs            = db.relationship('CSR', backref='office', lazy='joined')
    citizens        = db.relationship('Citizen', backref='office', lazy='joined')

    def __repr__(self):
        return '<Office Name:(name={self.office_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Office, self).__init__(**kwargs)
