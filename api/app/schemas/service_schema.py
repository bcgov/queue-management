from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Service
from qsystem import db

class ServiceSchema(ModelSchema):

    service_id              = fields.Int(dump_only=True)
    service_code            = fields.Str(dump_only=True)
    service_name            = fields.Str(dump_only=True)
    service_desc            = fields.Str(dump_only=True)
    parent_id               = fields.Int(dump_only=True)
    deleted                 = fields.DateTime(dump_only=True)
    prefix                  = fields.Str(dump_only=True)
    display_dashboard_ind   = fields.Int(dump_only=True)
    actual_service_ind      = fields.Int(dump_only=True)