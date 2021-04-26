from management import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    """Users table"""
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), default=False)
    email_confirmed_at = db.Column(db.DateTime())
    is_active = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return self.business_name
