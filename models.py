from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    income = db.Column(db.Float, nullable=False)
    splitting = db.Column(db.Integer, nullable=False)
    savings_id = db.Column(db.Integer, db.ForeignKey('savings.id'))  # <-- FK changed here
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.budget_id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    savings = db.relationship('Savings', backref='user', lazy=True)
    budget = db.relationship('Budget', backref='user', lazy=True)

    

class Budget(db.Model):
    budget_id = db.Column(db.Integer, primary_key=True)
    curr_total_budget = db.Column(db.Float, nullable=False)
    acc_id = db.Column(db.Integer, db.ForeignKey('accommodation.acc_id'))
    ent_id = db.Column(db.Integer, db.ForeignKey('entertainment.ent_id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'))
    trs_id = db.Column(db.Integer, db.ForeignKey('transportation.trs_id'))
    subs_id = db.Column(db.Integer, db.ForeignKey('subscription.subs_id'))
    other_id = db.Column(db.Integer, db.ForeignKey('other.other_id'))

    accommodation = db.relationship('Accommodation', backref='budget', lazy=True)
    entertainment = db.relationship('Entertainment', backref='budget', lazy=True)
    food = db.relationship('Food', backref='budget', lazy=True)
    transportation = db.relationship('Transportation', backref='budget', lazy=True)
    subscription = db.relationship('Subscription', backref='budget', lazy=True)
    other = db.relationship('Other', backref='budget', lazy=True)

class Accommodation(db.Model):
    acc_id = db.Column(db.Integer, primary_key=True)
    acc_budget = db.Column(db.Float, nullable=False)
    acc_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)

class Entertainment(db.Model):
    ent_id = db.Column(db.Integer, primary_key=True)
    ent_budget = db.Column(db.Float, nullable=False)
    ent_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)

class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    food_budget = db.Column(db.Float, nullable=False)
    food_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)

class Transportation(db.Model):
    trs_id = db.Column(db.Integer, primary_key=True)
    trs_budget = db.Column(db.Float, nullable=False)
    trs_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)


class Subscription(db.Model):
    subs_id = db.Column(db.Integer, primary_key=True)
    subs_budget = db.Column(db.Float, nullable=False)
    subs_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)


class Other(db.Model):
    other_id = db.Column(db.Integer, primary_key=True)
    other_budget = db.Column(db.Float, nullable=False)
    other_current = db.Column(db.Float, nullable=False)
    transaction = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)


class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curr_savings = db.Column(db.Float, nullable=False)
    saving_goal = db.Column(db.Float, nullable=True)  # <-- New field added
    date = db.Column(db.DateTime, nullable=True)
    detail = db.Column(db.Text, nullable=True)

class SavingsTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    savings_id = db.Column(db.Integer, db.ForeignKey('savings.id'), nullable=False)  # <-- fix here
    action = db.Column(db.String(10), nullable=False)  # 'save' or 'spend'
    amount = db.Column(db.Float, nullable=False)
    detail = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    savings = db.relationship('Savings', backref=db.backref('transactions', lazy=True))


class BudgetTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'accommodation', 'food', etc.
    amount = db.Column(db.Float, nullable=False)
    detail = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='budget_transactions')

class Loan(db.Model):
    __tablename__ = 'loan'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('loans', lazy=True))