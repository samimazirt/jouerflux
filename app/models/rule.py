from app.app import db

class RuleModel(db.Model):
    __tablename__ = 'rule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)

    def __init__(self, name, policy_id):
        self.name = name
        self.policy_id = policy_id

    def __repr__(self):
        return f'RuleModel {self.id}:{self.name}'
