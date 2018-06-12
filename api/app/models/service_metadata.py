from flask_restplus import fields
from qsystem import api, db
from base import Base 

class ServiceMetaDataTable(MyBase, Base, db.model):

    model = api.model('ServiceMetaDataTable' {
        'service_id' : fields.Integer,
        'metadata_id' : fields.Integer
        })

    service_id = db.Column(db.BigInteger)
    metadata_id = db.Column(db.BigInteger)

    # TODO do this need repr for testing?

    def __init__(self, service_id, metadata_id):
        self.service_id = service_id
        self.metadata_id = metadata_id

    def json(self, service_id, metadata_id):
        return {"service_id" : self.service_id, "metadata_id" : metadata_id}