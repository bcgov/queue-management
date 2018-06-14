from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String, DateTime

class Service(Base):

    model = api.model('Service', {
        'service_id' : fields.Integer,
        'service_code' : fields.String,
        'service_name' : fields.String,
        'service_desc' : feilds.String,
        'parent_id' : fields.Integer,
        'deleted' : fields.String,
        'prefix' : fields.String,
        'display_dashboard' : fields.Integer,
        'actual_service' : fields.Integer
        })

    service_id          = db.Columm(db.BigInteger, primary_key=True, autoincrement=True)
    service_code        = db.Columm(db.String(50))
    service_name        = db.Columm(db.String(500))
    service_desc        = db.Column(db.String(2000))
    # TODO - CFMS Data Dictionary says parent_ID is a FK to service_id. Please review.
    parent_id           = db.Column(db.BigInteger, db.ForeignKey('service_id'))
    deleted             = db.Column(db.DateTime, nullable=True)
    prefix              = db.Columm(db.String(10))
    display_dashboard   = db.Columm(db.Integer)
    actual_service      = db.Columm(db.Integer)

    def __repr__(self, service_name):
        return '<Service Name: %r>' % self.service_name

    args = {'service_id': 'service_id',
            'service_code': 'service_code',
            'service_name': 'service_name',
            'service_desc': 'service_desc',
            'parent_id': 'parent_id',
            'deleted': 'deleted',
            'prefix': 'prefix',
            'display_dashboard': 'display_dashboard',
            'actual_service': 'actual_service'}

    def __init__(self, **args):
        self.service_id         = args['service_id']
        self.service_code       = args['service_code']
        self.service_name       = args['service_name']
        self.service_desc       = args['service_desc']
        self.parent_id          = args['parent_id']
        self.deleted            = args['deleted']
        self.prefix             = args['prefix']
        self.display_dashboard  = args['display_dashboard']
        self.actual_service     = args['actual_service']

    json_args = {'service_id': "service_id", 
                 'service_code': "service_code", 
                 'service_name': "service_name",
                 'service_desc': "service_desc", 
                 'parent_id': "parent_id", 
                 'deleted': "deleted", 
                 'prefix': "prefix", 
                 'display_dashboard': "display_dashboard", 
                 'actual_service': "actual_service"}

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