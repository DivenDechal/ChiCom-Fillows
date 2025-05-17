from flask import Blueprint, request, flash, redirect, url_for, jsonify
from models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

BP_auth = Blueprint('BP_auth', __name__)

@BP_auth.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})

@BP_auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        monthly_income = float(request.form.get('monthly_income', 0))
        saving_percentage = int(request.form.get('saving_percentage', 0))

        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return redirect(url_for('BP.signup'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('BP.signup'))

        # Check for existing user
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('BP.signup'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('BP.signup'))

        # Create and save user
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