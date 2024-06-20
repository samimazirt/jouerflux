from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.models.rule import RuleModel
from app.app import db

ns_rule = Namespace('rule', description='Rule operations')

rule_model = ns_rule.model('Rule', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a rule'),
    'name': fields.String(required=True, description='The rule name'),
    'policy_id': fields.Integer(required=True, description='The policy ID')
})

def admin_required(f):
    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if current_user.admin is not True:
            return {"message": "Admin access required"}, 403
        return f(*args, **kwargs)
    return wrap

@ns_rule.route('/')
class RuleList(Resource):
    @ns_rule.expect(rule_model, validate=True)
    @ns_rule.response(201, 'Rule added')
    @admin_required
    def post(self):
        data = request.json
        new_rule = RuleModel(name=data['name'], policy_id=data['policy_id'])
        db.session.add(new_rule)
        db.session.commit()
        return {"message": "Rule added"}, 201

    @ns_rule.marshal_list_with(rule_model, envelope='rules')
    @login_required
    def get(self):
        rules = RuleModel.query.all()
        return rules

@ns_rule.route('/<int:id>')
@ns_rule.response(404, 'Rule not found')
class RuleResource(Resource):
    @ns_rule.response(200, 'Rule deleted')
    @admin_required
    def delete(self, id):
        rule = RuleModel.query.get(id)
        if not rule:
            return {"message": "Rule not found"}, 404
        db.session.delete(rule)
        db.session.commit()
        return {"message": "Rule deleted"}