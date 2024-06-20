from app.app import db

class RuleModel(db.Model):
    __tablename__ = 'rule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    source_ip = db.Column(db.String(80), nullable=False)
    destination_ip = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(10), nullable=False)

    def __init__(self, name, policy_id, source_ip, destination_ip, action):
        self.name = name
        self.policy_id = policy_id
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.action = action

    def __repr__(self):
        return f'RuleModel {self.id}:{self.name}'
