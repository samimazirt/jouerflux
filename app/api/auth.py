from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.app import db
from app.models.user import UserModel

ns_auth = Namespace('auth', description='Authentication related operations')

# Define the model for API documentation
user_model = ns_auth.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'admin': fields.Boolean(description='Is admin or not')
})

login_model = ns_auth.model('Login', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@ns_auth.route('/register')
class Register(Resource):
    @ns_auth.expect(user_model)
    @ns_auth.response(201, 'User successfully registered')
    def post(self):
        data = request.get_json()
        new_user = UserModel(username=data['username'], admin=data.get('admin'))
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered"}, 201

@ns_auth.route('/login')
class Login(Resource):
    @ns_auth.expect(login_model)
    @ns_auth.response(200, 'Logged in successfully')
    @ns_auth.response(401, 'Invalid credentials')
    def post(self):
        data = request.get_json()
        user = UserModel.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            return {"message": "Logged in"}, 200
        return {"message": "Invalid credentials"}, 401

@ns_auth.route('/logout')
class Logout(Resource):
    @login_required
    def post(self):
        """Logout the current user"""
        logout_user()
        return {"message": "Logged out successfully"}, 200

@ns_auth.route('/me')
class Me(Resource):
    @ns_auth.marshal_with(user_model)
    @login_required
    def get(self):
        """Get current user"""
        return current_user
