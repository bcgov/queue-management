from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from .office import Office
from sqlalchemy import BigInteger, Integer, String, DateTime

class Service(Base):

    service_metadata  = db.Table('service_metadata',
                            db.Column('service_id', db.Integer, 
                                      db.ForeignKey('service.service_id'), primary_key=True),
                            db.Column('metadata_id', db.Integer,
                                      db.ForeignKey('metadata.metadata_id'), primary_key=True)
    )

    model = api.model('Service', {
        'service_id': fields.Integer,
        'service_code': fields.String,
        'service_name': fields.String,
        'service_desc': fields.String,
        'parent_id': fields.Integer,
        'deleted': fields.String,
        'prefix': fields.String,
        'display_dashboard': fields.Integer,
        'actual_service': fields.Integer
        })

    service_id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_code        = db.Column(db.String(50), nullable=True)
    service_name        = db.Column(db.String(500))
    service_desc        = db.Column(db.String(2000), nullable=True)
    parent_id           = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=True)
    deleted             = db.Column(db.DateTime, nullable=True)
    prefix              = db.Column(db.String(10), nullable=True)
    display_dashboard   = db.Column(db.Integer, nullable=True)
    actual_service      = db.Column(db.Integer)

    offices             = db.relationship("Office", secondary=Office.office_service, back_populates="services")
    service_reqs        = db.relationship('ServiceReq', backref='service', lazy=False)
    Services            = db.relationship('Service', backref='parent', lazy=False)
    # meta data is a reserved sqlalchemy keyword
    metadatas           = db.relationship("Metadata", secondary=service_metadata, back_populates="services")

    def __repr__(self, service_name):
        return '<Service Name: %r>' % self.service_name

    def __init__(self, **kwargs):
        super(Service, self).__init__(**kwargs)

    def json(self, **json_args):
        return {json_args['service_id']: self.service_id,
                json_args['service_code']: self.service_code,
                json_args['service_name']: self.service_name,
                json_args['service_desc']: self.service_desc,
                json_args['parent_id']: self.parent_id,
                json_args['deleted']: self.deleted,
                json_args['prefix']: self.prefix,
                json_args['display_dashboard']: self.display_dashboard,
                json_args['actual_service']: self.actual_service}