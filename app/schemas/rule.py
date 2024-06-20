from marshmallow import fields
from app.app import ma
from app.models.rule import RuleModel

class RuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RuleModel
        load_instance = True
        unknown = INCLUDE
        field = ('id', 'name', 'policy_id')

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    policy_id = fields.Integer(required=True)
