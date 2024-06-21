from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.models.policy import PolicyModel
from app.app import db
from app.schemas.policy import PolicySchema
from marshmallow import ValidationError
from app.core.policy_service import create_policy, update_policy, delete_policy
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)
ns_policy = Namespace('policy', description='Policy operations')

policy_model = ns_policy.model('Policy', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a policy'),
    'name': fields.String(required=True, description='The policy name'),
    'firewall_id': fields.Integer(required=True, description='The firewall ID')
})

create_policy_model = ns_policy.model('Policy', {
    'name': fields.String(required=True, description='The policy name'),
    'firewall_id': fields.Integer(required=True, description='The firewall ID')
})

update_policy_model = ns_policy.clone('UpdatePolicy', create_policy_model)

def admin_required(f):
    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if current_user.admin is not True:
            return {"message": "Admin access required"}, 403
        return f(*args, **kwargs)
    return wrap

policy_schema = PolicySchema()
policies_schema = PolicySchema(many=True)

@ns_policy.route('/')
class PolicyList(Resource):
    @ns_policy.expect(create_policy_model, validate=True)
    @ns_policy.response(201, 'Policy added')
    @admin_required
    def post(self):
        data = request.json
        res, error = create_policy(data, policy_schema)
        if error:
            return res, 400
        logger.info(f"Create policy on a firewall {data['firewall_id']}")
        return policy_schema.dump(res), 201


    @ns_policy.marshal_list_with(policy_model, envelope='policies')
    @login_required
    def get(self):
        logger.info(f"Get policies")

        policies = PolicyModel.query.all()
        return policies_schema.dump(policies)

@ns_policy.route('/<int:id>')
@ns_policy.response(404, 'Policy not found')
class PolicyResource(Resource):
    @ns_policy.response(200, 'Policy deleted')
    @admin_required
    def delete(self, id):
        logger.info(f"Delete policy")
        res, errors = delete_policy(id)
        if errors:
            return errors, 400
        return res, 204

    @ns_policy.marshal_list_with(policy_model)
    @login_required
    def get(self, id):
        policy = PolicyModel.query.get(id)
        if not policy:
            return {"message": "Policy not found"}, 404
        logger.info(f"Getting policy with id {id}")
        return policy_schema.dump(policy), 200
    
    @ns_policy.expect(update_policy_model, validate=True)
    @ns_policy.response(200, 'Policy updated')
    @admin_required
    def put(self, id):
        data = request.json
        updated_policy, errors = update_policy(id, data, policy_schema)
        if errors:
            return errors, 400
        return policy_schema.dump(updated_policy), 200