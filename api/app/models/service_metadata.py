from flask_restplus import fields
from qsystem import api, db
from .base import Base 

class ServiceMetaData(Base):

    model = api.model('ServiceMetaData', {
        'service_id' : fields.Integer,
        'metadata_id' : fields.Integer
        })

    service_id  = db.Column(db.BigInteger, primary_key=True, db.ForeignKey('service.service_id'))
    metadata_id = db.Column(db.BigInteger, primary_key=True, db.ForeignKey('metadata.metadata_id'))

    # TODO do this need repr for testing?

    def __init__(self, service_id, metadata_id):
        self.service_id     = service_id
        self.metadata_id    = metadata_id

    def json(self, service_id, metadata_id):
        return {"service_id" : self.service_id, 
                "metadata_id" : metadata_id}