from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#from app.models import Service
from sqlalchemy import BigInteger, String

class MetaData(Base):

    model = api.model('MetaData', {
        'metadata_id': fields.Integer,
        'meta_text': fields.String
        })

    metadata_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meta_text       = db.Column(db.String(100))

    #services        = db.relationship("Service", secondary=Service.service_metadata, back_populates="metadata")

    def __repr__(self, meta_text):
        return '<Meta Text: %r>' % self.meta_text

    def __init__(self, **kwargs):
        super(MetaData, self).__init__(**kwargs)

    def json(self, metadata_id, meta_text):
        return {"metadata_id" : self.metadata_id, 
                "meta_text" : self.meta_text}