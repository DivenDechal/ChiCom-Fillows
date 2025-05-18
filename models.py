from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Savings(db.Model):
    __tablename__ = 'savings'
    savings_trans_id = db.Column(db.Integer, primary_key=True)
    total_saved = db.Column(db.Float, default=0.0)

    # One-to-many (one savings to many users)
    users = db.relationship('User', backref='savings', lazy=True)


class Budget(db.Model):
    __tablename__ = 'budget'
    budget_id = db.Column(db.Integer, primary_key=True)
    total_budget = db.Column(db.Float, default=0.0)

    # One-to-many (one budget to many users)
    users = db.relationship('User', backref='budget', lazy=True)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Hashed password
    income = db.Column(db.Float, nullable=False)
    splitting = db.Column(db.Integer, nullable=False)

    savings_id = db.Column(db.Integer, db.ForeignKey('savings.savings_trans_id'), nullable=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.budget_id'), nullable=True)

    def set_password(self, password_plain):
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    def __repr__(self):
        return f"<User {self.username}>"
