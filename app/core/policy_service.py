from app.models.policy import PolicyModel
from app.models.firewall import FirewallModel
from app.models.rule import RuleModel
from app.app import db
from marshmallow import ValidationError
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)

def create_policy(data, policy_schema):
    logger.info("creating the policy")
    try:
        validated_data = policy_schema.load(data)
    except ValidationError as err:
        logger.error("invalid input/schema")
        return {"message": "Validation error", "errors": err.messages}

    firewall = FirewallModel.query.get(validated_data['firewall_id'])
    if not firewall:
        logger.error("FireWall with this id not found")
        return {"message": "Firewall not found"}, 404

    new_policy = PolicyModel(name=validated_data['name'], firewall_id=validated_data['firewall_id'])
    db.session.add(new_policy)
    db.session.commit()
    return new_policy, None


def update_policy(policy_id, data, policy_schema):
    logger.info("updating the policy")
    try:
        validated_data = policy_schema.load(data)
    except ValidationError as err:
        logger.error("invalid input/schema")
        return {"message": "Validation error", "errors": err.messages}

    policy = PolicyModel.query.get(policy_id)
    if not policy:
        logger.error("policy not found")
        return {"message": "Policy not found"}, 404

    if 'firewall_id' in validated_data:
        firewall = FirewallModel.query.get(validated_data['firewall_id'])
        if not firewall:
            logger.error("policy not found")
            return {"message": "Firewall not found"}, 404

    for key, value in validated_data.items():
        setattr(policy, key, value)

    db.session.commit()
    return policy, None

def delete_policy(policy_id):
    logger.info("deleting policy")

    policy = PolicyModel.query.get(policy_id)

    if not policy.rules:
        logger.info("no rules in the policy")

    for rule in policy.rules:
        logger.info(f"deleting rule with ID {rule.id} for policy id {policy_id}")
        db.session.delete(rule)
    
    
    if policy:
        logger.info(f"deleting policy with ID {policy_id}")
        db.session.delete(policy)
        db.session.commit()
        return {"message": f"Policy {policy_id} and rules deleted"}, None
    else:
        logger.warning(f"Policy with ID {policy_id} not found")
        return {"message": f"Policy {policy_id} not found"}, 404