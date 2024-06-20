from app.app import db

class PolicyModel(db.Model):
    __tablename__ = 'policy'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    firewall_id = db.Column(db.Integer, db.ForeignKey('firewall.id'), nullable=False)
    #rules = db.relationship('RuleModel', backref='policy', lazy=True)

    def __init__(self, name, firewall_id):
        self.name = name
        self.firewall_id = firewall_id

    def __repr__(self):
        return f'PolicyModel {self.id}:{self.name}'
