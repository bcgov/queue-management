from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger

class OfficeService(Base):

    model = api.model('OfficeService', {
        'office_id' : fields.Integer,
        'service_id' : fields.Integer
        })

    office_id   = db.Column(db.BigInteger)
    service_id  = db.Column(db.BigInteger)

    def __init__(self, office_id, service_id):
        self.office_id  = office_id
        self.service_id = service_id

    def json(self, office_id, service_id):
        return {"office_id" : self.office_id, 
                "service_id" : self.service_id}