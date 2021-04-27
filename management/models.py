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
    merchants = db.relationship('Merchants', backref='merchant', lazy=True)
    customers = db.relationship('Customers', backref='customer', lazy=True)

    def __repr__(self):
        return self.business_name

    def get_date(self):
        date = self.email_confirmed_at.strftime('%B %d, %Y')
        return date


class Merchants(db.Model):
    """Merchants table"""
    id = db.Column(db.Integer, primary_key=True)
    merchant_name = db.Column(db.String(50), unique=True, nullable=False)
    contact_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.merchant_name


class Customers(db.Model):
    """Merchants table"""
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.customer_name
