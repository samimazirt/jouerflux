from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.app import db
from app.models.firewall import FirewallModel
from app.schemas.firewall import FirewallSchema
from marshmallow import ValidationError
from app.core.firewall_service import create_firewall, update_firewall, delete_firewall
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

update_firewall_model = ns_fw.clone('UpdateFirewall', create_firewall_model)


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
        res, errors = delete_firewall(id)
        if errors:
            return errors, 400
        return res, 204

    @ns_fw.doc('get_firewall')
    @ns_fw.marshal_list_with(firewall_model)
    @login_required
    def get(self, id):
        logger.info(f"Get firewall by id")
        firewall = FirewallModel.query.get(id)
        if not firewall:
            return {"message": "Firewall not found"}, 404
        return firewall_schema.dump(firewall), 200

    @ns_fw.expect(update_firewall_model, validate=True)
    @ns_fw.response(200, 'Policy updated')
    @admin_required
    def put(self, id):
        data = request.json
        updated_firewall, errors = update_firewall(id, data, firewall_schema)
        if errors:
            return errors, 400
        return firewall_schema.dump(updated_firewall), 200