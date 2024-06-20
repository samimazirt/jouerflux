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
