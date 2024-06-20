from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.app import db
from app.models.firewall import FirewallModel
from app.schemas.firewall import FirewallSchema
from marshmallow import ValidationError
from app.core.firewall_service import create_firewall
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)

ns_fw = Namespace('firewalls', description='Firewall related operations')

firewall_model = ns_fw.model('Firewall', {
    'id': fields.Integer(readOnly=True, description='unique identifier of a firewall'),
    'name': fields.String(required=True, description='Firewall name')
})

create_firewall_model = ns_fw.model('Firewall', {
    'name': fields.String(required=True, description='Firewall name')
})

def admin_required(f):
    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if current_user.admin is not True:
            return {"message": "Admin access required"}, 403
        return f(*args, **kwargs)
    return wrap

firewall_schema = FirewallSchema()
firewalls_schema = FirewallSchema(many=True)

@ns_fw.route('')
class FirewallList(Resource):
    @ns_fw.doc('list_firewalls')
    @ns_fw.marshal_list_with(firewall_model)
    @login_required
    def get(self):
        logger.info(f"Get all frirewalls")
        firewalls = FirewallModel.query.all()
        return firewalls_schema.dump(firewalls)

    @ns_fw.doc('create_firewall')
    @ns_fw.expect(create_firewall_model)
    @ns_fw.marshal_with(firewall_model, code=201)
    @admin_required
    def post(self):
        logger.info(f"Create a firewall")
        data = request.json
        try:
            validated_data = firewall_schema.load(data)
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        new_firewall, errors = create_firewall(validated_data)
        if errors:
            return errors, 400
        return firewall_schema.dump(new_firewall), 201

@ns_fw.route('/<int:id>')
@ns_fw.response(404, 'Firewall not found')
class FirewallResource(Resource):
    @ns_fw.doc('delete_firewall')
    @ns_fw.response(204, 'Firewall successfully deleted')
    @admin_required
    def delete(self, id):
        logger.info(f"Delete firewall")
        firewall = FirewallModel.query.get(id)
        if not firewall:
            return {"message": "Firewall not found"}, 404
        db.session.delete(firewall)
        db.session.commit()
        return '', 204

    @ns_fw.doc('get_firewall')
    @ns_fw.marshal_list_with(firewall_model)
    @login_required
    def get(self, id):
        logger.info(f"Get firewall by id")
        firewall = FirewallModel.query.get(id)
        if not firewall:
            return {"message": "Firewall not found"}, 404
        return firewall_schema.dump(firewall), 200

