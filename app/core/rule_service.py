from app.models.rule import RuleModel
from app.models.policy import PolicyModel
from app.app import db
from marshmallow import ValidationError
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)

def create_rule(data, rule_schema):
    logging.info("creating the rule")
    try:
        validated_data = rule_schema.load(data)
    except ValidationError as err:
        logger.error("invalid input/schema")
        return {"message": "Validation error", "errors": err.messages}

    policy = PolicyModel.query.get(validated_data['policy_id'])
    if not policy:
        logger.error("Policy not found")
        return {"message": "Policy not found"}, 404

    new_rule = RuleModel(name=validated_data['name'], policy_id=validated_data['policy_id'], source_ip=validated_data['source_ip'],
        destination_ip=validated_data['destination_ip'],action=validated_data['action'])
    db.session.add(new_rule)
    db.session.commit()
    return new_rule, None
