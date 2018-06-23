from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#from app.models import Service
from sqlalchemy import BigInteger, String

class MetaData(Base):

    metadata_id     = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    meta_text       = db.Column(db.String(100), nullable=False)

    #services        = db.relationship("Service", secondary=Service.service_metadata, back_populates="metadata")

    def __repr__(self):
        return '<Meta Data:(name={self.meta_text!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(MetaData, self).__init__(**kwargs)
