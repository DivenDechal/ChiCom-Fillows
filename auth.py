from flask import Blueprint, request, jsonify
from models import db, User
import re

BP_auth = Blueprint('BP_auth', __name__)

@BP_auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        income_raw = request.form.get('monthly_income', '0')
        saving_raw = request.form.get('saving_percentage', '0')

        # Validate required fields
        if not all([username, password, confirm_password, income_raw, saving_raw]):
            return jsonify(success=False, message="All fields are required."), 400

        # Password checks
        if password != confirm_password:
            return jsonify(success=False, message="Passwords do not match."), 400
        if len(password) < 6:
            return jsonify(success=False, message="Password must be at least 6 characters long."), 400

        # Validate numeric fields
        try:
            monthly_income = float(income_raw)
            saving_percentage = int(saving_raw)
            if monthly_income < 0 or not (0 <= saving_percentage <= 100):
                return jsonify(success=False, message="Income must be positive and saving percentage must be 0–100."), 400
        except ValueError:
            return jsonify(success=False, message="Invalid input for income or saving percentage."), 400

        # Check for existing user
        if User.query.filter_by(username=username).first():
            return jsonify(success=False, message="Username already exists."), 409

        # Create and save new user
        new_user = User(
            username=username,
            income=monthly_income,
            splitting=saving_percentage
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(success=True, message="Account created successfully! Please sign in."), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message="Server error. Please try again."), 500
