from app.models.rule import RuleModel
from app.models.policy import PolicyModel
from app.app import db
from marshmallow import ValidationError

def create_rule(data, rule_schema):
    """Create a new rule after validating and checking if the policy exists."""
    try:
        validated_data = rule_schema.load(data)
    except ValidationError as err:
        return {"message": "Validation error", "errors": err.messages}

    policy = PolicyModel.query.get(validated_data['policy_id'])
    if not policy:
        return {"message": "Policy not found"}, 404

    new_rule = RuleModel(name=validated_data['name'], policy_id=validated_data['policy_id'])
    db.session.add(new_rule)
    db.session.commit()
    return new_rule, None
