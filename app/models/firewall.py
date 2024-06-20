from app.app import db

class FirewallModel(db.Model):
    __tablename__ = 'firewall'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    #policies = db.relationship('PolicyModel', backref='firewall', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'FirewallModel {self.id}:{self.name}'
