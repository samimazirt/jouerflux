from marshmallow import Schema, fields, validate, ValidationError
from app.app import ma
from app.models.rule import RuleModel
import ipaddress
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        logger.error("invalid ip")
        raise ValidationError(f"Invalid IP address: {ip}")

class RuleSchema(ma.SQLAlchemyAutoSchema):

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    policy_id = fields.Integer(required=True)
    source_ip = fields.Str(required=True, validate=validate_ip)
    destination_ip = fields.Str(required=True, validate=validate_ip)
    action = fields.Str(required=True, validate=validate.OneOf(['ALLOW', 'DENY']))
