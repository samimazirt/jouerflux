from marshmallow import fields
from app.app import ma
from app.models.policy import PolicyModel

class PolicySchema(ma.SQLAlchemyAutoSchema):

    name = fields.Str(required=True)
    firewall_id = fields.Integer(required=True)
