from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.models.policy import PolicyModel
from app.app import db
from app.schemas.policy import PolicySchema
from marshmallow import ValidationError
from app.core.policy_service import create_policy

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
        return policy_schema.dump(res), 201


    @ns_policy.marshal_list_with(policy_model, envelope='policies')
    @login_required
    def get(self):
        policies = PolicyModel.query.all()
        return policies_schema.dump(policies)

@ns_policy.route('/<int:id>')
@ns_policy.response(404, 'Policy not found')
class PolicyResource(Resource):
    @ns_policy.response(200, 'Policy deleted')
    @admin_required
    def delete(self, id):
        policy = PolicyModel.query.get(id)
        if not policy:
            return {"message": "Policy not found"}, 404
        db.session.delete(policy)
        db.session.commit()
        return {"message": "Policy deleted"}

    @ns_policy.marshal_list_with(policy_model)
    @login_required
    def get(self, id):
        policy = PolicyModel.query.get(id)
        if not policy:
            return {"message": "Policy not found"}, 404
        return policy_schema.dump(policy), 200