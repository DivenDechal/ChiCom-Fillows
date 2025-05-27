from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models import db, User, Budget, Account, Entertainment, Food, Transportation, Subscription, Other, SavingsTransaction, Savings
from datetime import datetime
from functools import wraps

BP = Blueprint('BP', __name__)

def login_required_manual(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # If AJAX request, return JSON error, else redirect
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(success=False, message="Not logged in"), 401
            return redirect(url_for('BP.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

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
@login_required_manual
def budget():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    if not user.budget:
        budget = Budget(curr_total_budget=user.income)
        
        account = Account(acc_budget=0.0, acc_current=0.0)
        entertainment = Entertainment(ent_budget=0.0, ent_current=0.0)
        food = Food(food_budget=0.0, food_current=0.0)
        transportation = Transportation(trs_budget=0.0, trs_current=0.0)
        subscription = Subscription(subs_budget=0.0, subs_current=0.0)
        other = Other(other_budget=0.0, other_current=0.0)
        
        db.session.add_all([account, entertainment, food, transportation, subscription, other])
        db.session.commit()
        
        budget.account = account
        budget.entertainment = entertainment
        budget.food = food
        budget.transportation = transportation
        budget.subscription = subscription
        budget.other = other

        db.session.add(budget)
        db.session.commit()
        
        user.budget = budget
        db.session.commit()
    else:
        budget = user.budget

    categories = {
        "Accommodation and Utilities": {
            "budget": budget.account.acc_budget if budget.account else 0,
            "current": budget.account.acc_current if budget.account else 0
        },
        "Entertainment": {
            "budget": budget.entertainment.ent_budget if budget.entertainment else 0,
            "current": budget.entertainment.ent_current if budget.entertainment else 0
        },
        "Food and Clothes": {
            "budget": budget.food.food_budget if budget.food else 0,
            "current": budget.food.food_current if budget.food else 0
        },
        "Transportation": {
            "budget": budget.transportation.trs_budget if budget.transportation else 0,
            "current": budget.transportation.trs_current if budget.transportation else 0
        },
        "Subscription": {
            "budget": budget.subscription.subs_budget if budget.subscription else 0,
            "current": budget.subscription.subs_current if budget.subscription else 0
        },
        "Others": {
            "budget": budget.other.other_budget if budget.other else 0,
            "current": budget.other.other_current if budget.other else 0
        }
    }

    category_labels = list(categories.keys())
    category_values = [cat["current"] or 0 for cat in categories.values()]

    if not any(category_values):
        category_labels = ["No Data"]
        category_values = [1]

    return render_template(
        'budget.html',
        total_budget=budget.curr_total_budget or 0,
        categories=categories,
        category_labels=category_labels,
        category_values=category_values
    )

@BP.route('/savings', methods=['GET'])
@login_required_manual
def savings():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    savings = Savings.query.get(user.savings_id) if user.savings_id else None

    return render_template(
    'savings.html',
    savings=savings,
    curr_savings=savings.curr_savings if savings else 0,
    saving_goal=savings.saving_goal if savings and savings.saving_goal else 0,
    transactions=[]  # <-- avoids error in Jinja template
)