from app.models.firewall import FirewallModel
from app.models.policy import PolicyModel
from app.app import db
from marshmallow import ValidationError
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)

def create_firewall(validated_data):
    logger.info("creating the firewall")

    new_firewall = FirewallModel(name=validated_data['name'])
    db.session.add(new_firewall)
    db.session.commit()
    return new_firewall, None


def update_firewall(firewall_id, data, firewall_schema):
    logger.info("updating the firewall")
    try:
        validated_data = firewall_schema.load(data)
    except ValidationError as err:
        logger.error("invalid input/schema")
        return {"message": "Validation error", "errors": err.messages}

    firewall = FirewallModel.query.get(firewall_id)
    if not firewall:
        logger.error("firewall not found")
        return {"message": "firewall not found"}, 404

    for key, value in validated_data.items():
        setattr(firewall, key, value)

    db.session.commit()
    return firewall, None

def delete_firewall(firewall_id):
    logger.info("deleting firewall")
    policies = PolicyModel.query.filter_by(firewall_id=firewall_id).all()

    if not policies:
        logger.info(f"no policies found for firewall ID {firewall_id}")

    for policy in policies:
        logger.info(f"deleting policy with ID {policy.id} for firewall id {firewall_id}")
        db.session.delete(policy)
    
    firewall = FirewallModel.query.get(firewall_id)
    if firewall:
        logger.info(f"deleting firewall with ID {firewall_id}")
        db.session.delete(firewall)
        db.session.commit()
        return {"message": f"Firewall {firewall_id} and policies deleted"}, None
    else:
        logger.warning(f"Firewall with ID {firewall_id} not found")
        return {"message": f"Firewall {firewall_id} not found"}, 404