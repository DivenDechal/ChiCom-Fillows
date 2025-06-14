from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, User, Savings
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

BP = Blueprint('BP', __name__)

# View routes
@BP.route('/')
def home():
    return render_template('main.html', user=session.get('user'))

@BP.route('/login')
def login():
    return render_template('signin.html')

@BP.route('/signup')
def signup():
    return render_template('signup.html')

@BP.route('/budget')
def budget():
    return render_template('budget.html')

@BP.route('/debts')
def debts():
    return render_template('debts.html')

@BP.route('/saving')
def saving():
    if 'user_id' not in session:
        return redirect(url_for('BP.login'))

    user = User.query.get(session['user_id'])
    now = datetime.utcnow()

    last_saving = Savings.query.filter_by(user_id=user.id).order_by(Savings.date.desc()).first()
    already_added = last_saving and last_saving.date.year == now.year and last_saving.date.month == now.month

    if not already_added:
        increment = user.income * (user.splitting / 100)
        curr_savings = last_saving.curr_savings if last_saving else 0

        new_savings = Savings(
            curr_savings=curr_savings + increment,
            transaction="Auto Monthly Transfer",
            date=now,
            detail=f"Monthly auto-saving for {now.strftime('%B %Y')}",
            user_id=user.id
        )
        db.session.add(new_savings)
        db.session.commit()

    return render_template('savings.html')

@BP.route('/account')
def account():
    return render_template('account.html')

# Auth routes
@BP.route('/signin', methods=['POST'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        flash('Invalid email or password', 'error')
        return redirect(url_for('BP.login'))
    
    session['user_id'] = user.id
    return redirect(url_for('BP.saving'))

@BP.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('BP.login'))

@BP.route('/signup', methods=['POST'])
def signup_post():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        monthly_income = float(request.form.get('monthly_income', 0))
        saving_percentage = int(request.form.get('saving_percentage', 0))

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
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('BP.login'))

    except ValueError:
        flash('Invalid input values', 'error')
        return redirect(url_for('BP.signup'))
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration', 'error')
        return redirect(url_for('BP.signup'))
