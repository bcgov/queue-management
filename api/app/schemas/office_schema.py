from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Office
from qsystem import db

class OfficeSchema(ModelSchema):

    office_id       = fields.Int()
    office_name     = fields.Str()
    office_number   = fields.Int()
    sb_id           = fields.Int()
    deleted         = fields.DateTime()