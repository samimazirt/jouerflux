from app.models.policy import PolicyModel
from app.models.firewall import FirewallModel
from app.app import db
from marshmallow import ValidationError

def create_policy(data, policy_schema):
    """Create a new policy after validating and checking if the firewall exists."""
    try:
        validated_data = policy_schema.load(data)
    except ValidationError as err:
        return {"message": "Validation error", "errors": err.messages}

    firewall = FirewallModel.query.get(validated_data['firewall_id'])
    if not firewall:
        return {"message": "Firewall not found"}, 404

    new_policy = PolicyModel(name=validated_data['name'], firewall_id=validated_data['firewall_id'])
    db.session.add(new_policy)
    db.session.commit()
    return new_policy, None
