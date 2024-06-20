from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from functools import wraps
from app.app import db
from app.models.firewall import FirewallModel
from app.schemas.firewall import FirewallSchema
from marshmallow import ValidationError

ns_fw = Namespace('firewalls', description='Firewall related operations')

# Define the model for API documentation
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
        """List all firewalls"""
        firewalls = FirewallModel.query.all()
        return firewalls_schema.dump(firewalls)

    @ns_fw.doc('create_firewall')
    @ns_fw.expect(create_firewall_model)
    @ns_fw.marshal_with(firewall_model, code=201)
    @admin_required
    def post(self):
        """Create a new firewall"""
        data = request.json
        try:
            validated_data = firewall_schema.load(data)
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        new_firewall = FirewallModel(name=validated_data['name'])
        db.session.add(new_firewall)
        db.session.commit()
        return firewall_schema.dump(new_firewall), 201

@ns_fw.route('/<int:id>')
@ns_fw.response(404, 'Firewall not found')
class FirewallResource(Resource):
    @ns_fw.doc('delete_firewall')
    @ns_fw.response(204, 'Firewall successfully deleted')
    @admin_required
    def delete(self, id):
        """Delete a firewall given its identifier"""
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
        """Retrieve a firewall given its identifier"""
        firewall = FirewallModel.query.get(id)
        if not firewall:
            return {"message": "Firewall not found"}, 404
        return firewall_schema.dump(firewall), 200

