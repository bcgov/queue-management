from flask_restplus import fields
from qsystem import api, db
from base import Base 

class Service(Base):

    model = api.model('Service' {
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
    parent_id           = db.Column(db.BigInteger)
    deleted             = db.Column(db.DateTime, nullable=True)
    prefix              = db.Columm(db.String(10))
    display_dashboard   = db.Columm(db.Integer)
    actual_service      = db.Columm(db.Integer)

    def __repr__(self, service_name):
        return '<Service Name: %r>' % self.service_name

    def __init__(self, service_id, service_code, service_name, service_desc, parent_id, 
                deleted, prefix, display_dashboard, actual_service)
        self.service_id         = service_id
        self.service_code       = service_code
        self.service_name       = service_name
        self.service_desc       = service_desc
        self.parent_id          = parent_id
        self.deleted            = deleted
        self.prefix             = prefix
        self.display_dashboard  = display_dashboard
        self.actual_service     = actual_service

    def json(json, service_id, service_code, service_name, service_desc, parent_id, deleted, 
            prefix, display_dashboard, actual_service)
        return {"service_id" : self.service_id, 
                "service_code" : self.service_code, 
                "service_name" : self.service_name,
                "service_desc" : self.service_desc, 
                "parent_id" : self.parent_id, 
                "deleted" : self.deleted, 
                "prefix" : self.prefix, 
                "display_dashboard" : self.display_dashboard, 
                "actual_service" : self.actual_service}