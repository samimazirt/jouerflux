from app.models.firewall import FirewallModel
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