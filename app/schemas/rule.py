from marshmallow import Schema, fields, validate
from app.app import ma
from app.models.rule import RuleModel

class RuleSchema(ma.SQLAlchemyAutoSchema):

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    policy_id = fields.Integer(required=True)
