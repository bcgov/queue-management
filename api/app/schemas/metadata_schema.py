from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import MetaData
from qsystem import db

class MetaDataSchema(ModelSchema):

    metadata_id     = fields.Int()
    meta_text       = fields.Str()