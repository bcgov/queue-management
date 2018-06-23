from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Permission
from qsystem import db

class PermissionSchema(ModelSchema):

    permission_id    = fields.Int()
    permission_code  = fields.Str()
    permission_desc  = fields.Str()