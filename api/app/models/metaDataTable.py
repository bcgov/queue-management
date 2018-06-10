from flask_restplus import fields
from qsystem import api, db
from base import Base 

class MetaDataTable(MyBase, Base, db.model):

    model = api.model('MetaDataTable' {
        'metadata_id' : fields.Integer,
        'meta_text' : fields.String
        })

    metadata_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    meta_text = db.Column(db.String(100))

    def __repr__(self, meta_text):
        return '<Meta Text: %r>' % self.meta_text

    def __init__(self, metadata_id, meta_text):
        self.metadata_id = metadata_id
        self.meta_text = meta_text

    def json(self, metadata_id, meta_text):
        return {"metadata_id" : self.metadata_id, "meta_text" : self.meta_text}