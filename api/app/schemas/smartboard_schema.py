from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import SmartBoard
from qsystem import db

class SmartBoardSchema(ModelSchema):

    sb_id       = fields.Int()
    sb_type     = fields.Str()