from flask import Blueprint, request, flash, redirect, url_for, jsonify, session
from models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from models import (
    db, User, Budget,
    Account, Entertainment, Food,
    Transportation, Subscription, Other, Savings
)

BP_auth = Blueprint('BP_auth', __name__)

@BP_auth.route('/signin', methods=['POST'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Invalid email or password', 'error')
        return redirect(url_for('BP.login'))

    session['user_id'] = user.id
    return redirect(url_for('BP.savings'))

@BP_auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('BP.login'))

@BP_auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        monthly_income = float(request.form.get('monthly_income', 0))
        saving_percentage = int(request.form.get('saving_percentage', 0))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('BP.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('BP.signup'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('BP.signup'))

        new_user = User(
            username=username,
            email=email,
            income=monthly_income,
            splitting=saving_percentage
        )
        new_user.set_password(password)
        db.session.add(new_user)

        account       = Account(acc_budget=0.0, acc_current=0.0)
        entertainment = Entertainment(ent_budget=0.0, ent_current=0.0)
        food          = Food(food_budget=0.0, food_current=0.0)
        transportation= Transportation(trs_budget=0.0, trs_current=0.0)
        subscription  = Subscription(subs_budget=0.0, subs_current=0.0)
        other         = Other(other_budget=0.0, other_current=0.0)

        db.session.add_all([account, entertainment, food,
                            transportation, subscription, other])
        db.session.flush()

        total_budget = monthly_income
        budget = Budget(
            curr_total_budget=total_budget,
            account=account,
            entertainment=entertainment,
            food=food,
            transportation=transportation,
            subscription=subscription,
            other=other
        )
        db.session.add(budget)
        db.session.flush()

        new_user.budget_id = budget.budget_id

        savings_goal = monthly_income * (saving_percentage / 100.0)
        savings = Savings(curr_savings=0.0, saving_goal=savings_goal)
        db.session.add(savings)
        db.session.flush()
        new_user.savings_id = savings.id

        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('BP.login'))

    except ValueError:
        db.session.rollback()
        flash('Invalid input values', 'error')
        return redirect(url_for('BP.signup'))

    except IntegrityError:
        db.session.rollback()
        flash('Database integrity error', 'error')
        return redirect(url_for('BP.signup'))

    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration', 'error')
        return redirect(url_for('BP.signup'))
