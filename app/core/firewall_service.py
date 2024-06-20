from app.models.firewall import FirewallModel
from app.app import db
from marshmallow import ValidationError

def create_firewall(validated_data):
    """Create a new firewall."""

    new_firewall = FirewallModel(name=validated_data['name'])
    db.session.add(new_firewall)
    db.session.commit()
    return new_firewall, None
