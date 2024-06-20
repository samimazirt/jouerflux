from app.app import ma
from app.models.policy import PolicyModel
from marshmallow import Schema, fields, validate


class PolicySchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    firewall_id = fields.Integer(required=True)
