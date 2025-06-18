from flask import Blueprint, request, flash, redirect, url_for, jsonify, session
from models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from models import (
    db, User, Budget,
    Accommodation, Entertainment, Food,
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

        # Create user
        new_user = User(
            username=username,
            email=email,
            income=monthly_income,
            splitting=saving_percentage
        )
        new_user.set_password(password)
        db.session.add(new_user)

        # Calculate savings
        savings_amount = monthly_income * (saving_percentage / 100)
        remaining_budget = monthly_income - savings_amount

        # Hardcoded budget splits
        acc_amt = remaining_budget * 0.30
        food_amt = remaining_budget * 0.20
        trs_amt = remaining_budget * 0.15
        ent_amt = remaining_budget * 0.15
        subs_amt = remaining_budget * 0.10
        other_amt = remaining_budget * 0.10

        accommodation = Accommodation(acc_budget=acc_amt, acc_current=0.0)
        entertainment = Entertainment(ent_budget=ent_amt, ent_current=0.0)
        food = Food(food_budget=food_amt, food_current=0.0)
        transportation = Transportation(trs_budget=trs_amt, trs_current=0.0)
        subscription = Subscription(subs_budget=subs_amt, subs_current=0.0)
        other = Other(other_budget=other_amt, other_current=0.0)

        db.session.add_all([accommodation, entertainment, food,
                            transportation, subscription, other])
        db.session.flush()

        budget = Budget(
            curr_total_budget=remaining_budget,
            accommodation=accommodation,
            entertainment=entertainment,
            food=food,
            transportation=transportation,
            subscription=subscription,
            other=other
        )
        db.session.add(budget)
        db.session.flush()
        new_user.budget_id = budget.budget_id

        # Savings object with full amount
        savings = Savings(
            curr_savings=savings_amount,
            saving_goal=savings_amount
        )
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

