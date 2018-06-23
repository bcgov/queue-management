from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Role
from qsystem import db

class RoleSchema(ModelSchema):

    role_id     = fields.Int()
    role_code   = fields.Str()
    role_desc   = fields.Str()