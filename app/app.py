from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_restx import Api
from app.config import config_by_name, Config
import logging

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_app(config_name='local'):
    app = Flask(__name__)
    
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)

    app_config = config_by_name[config_name]
    app_config.setup_logging()
    logger = logging.getLogger(__name__)

    api = Api(app, version='1.0', title='JouerFlux API', description='A simple API')

    with app.app_context():
        from app.models.user import UserModel
        from app.models.firewall import FirewallModel
        from app.models.policy import PolicyModel
        from app.models.rule import RuleModel

        @login_manager.user_loader
        def load_user(user_id):
            return UserModel.query.get(int(user_id))

        from app.api.firewall import ns_fw as firewall_ns
        from app.api.policy import ns_policy as policy_ns
        from app.api.rule import ns_rule as rule_ns
        from app.api.auth import ns_auth as auth_ns

        api.add_namespace(firewall_ns, path='/api/firewalls')
        api.add_namespace(policy_ns, path='/api/policies')
        api.add_namespace(rule_ns, path='/api/rules')
        api.add_namespace(auth_ns, path='/api/auth')

        db.create_all()

    return app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
