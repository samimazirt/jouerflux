from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.models.rule import RuleModel
from app.app import db
from app.schemas.rule import RuleSchema
from marshmallow import ValidationError
from app.core.rule_service import create_rule
from app.config import Config
import logging

Config.setup_logging()
logger = logging.getLogger(__name__)
ns_rule = Namespace('rule', description='Rule operations')

rule_model = ns_rule.model('Rule', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a rule'),
    'name': fields.String(required=True, description='The rule name'),
    'policy_id': fields.Integer(required=True, description='The policy ID')
})

create_rule_model = ns_rule.model('Rule', {
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

rule_schema = RuleSchema()
rules_schema = RuleSchema(many=True)

@ns_rule.route('/')
class RuleList(Resource):
    @ns_rule.expect(create_rule_model, validate=True)
    @ns_rule.response(201, 'Rule added')
    @admin_required
    def post(self):
        data = request.json
        res, error = create_rule(data, rule_schema)
        if error:
            return res, 400
        logger.info(f"Creating rule on policy {data['policy_id']}")
        return rule_schema.dump(res), 201


    @ns_rule.marshal_list_with(rule_model, envelope='rules')
    @login_required
    def get(self):
        logger.info(f"getting rules")
        rules = RuleModel.query.all()
        return rules_schema.dump(rules)

@ns_rule.route('/<int:id>')
@ns_rule.response(404, 'Rule not found')
class RuleResource(Resource):
    @ns_rule.response(200, 'Rule deleted')
    @admin_required
    def delete(self, id):
        rule = RuleModel.query.get(id)
        if not rule:
            return {"message": "Rule not found"}, 404
        logger.info(f"Deleting rule with id {id}")
        db.session.delete(rule)
        db.session.commit()
        return {"message": "Rule deleted"}

    @ns_rule.marshal_list_with(rule_model, envelope='rules')
    @login_required
    def get(self, id):
        rule = RuleModel.query.get(id)
        if not rule:
            return {"message": "Rule not found"}, 404
        logger.info(f"Getting Rule with id {id}")
        return rule_schema.dump(rule), 200