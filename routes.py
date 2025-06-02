from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models import db, User, Budget, Accommodation, Entertainment, Food, Transportation, Subscription, Other, SavingsTransaction, Savings
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
        
        accommodation = Accommodation(acc_budget=0.0, acc_current=0.0)
        entertainment = Entertainment(ent_budget=0.0, ent_current=0.0)
        food = Food(food_budget=0.0, food_current=0.0)
        transportation = Transportation(trs_budget=0.0, trs_current=0.0)
        subscription = Subscription(subs_budget=0.0, subs_current=0.0)
        other = Other(other_budget=0.0, other_current=0.0)
        
        db.session.add_all([accommodation, entertainment, food, transportation, subscription, other])
        db.session.commit()
        
        budget.accommodation = accommodation
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
            "budget": budget.accommodation.acc_budget if budget.accommodation else 0,
            "current": budget.accommodation.acc_current if budget.accommodation else 0
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


@BP.route('/savings', methods=['GET', 'POST'])
@login_required_manual
def savings():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    savings = Savings.query.get(user.savings_id) if user.savings_id else None
    budget = user.budget if user else None

    if request.method == 'POST':
        action = request.form.get('action')  # 'save' or 'spend'
        amount = float(request.form.get('amount', 0))
        detail = request.form.get('detail')
        date = datetime.now()

        if not savings or not budget:
            flash("Savings or Budget not set up.", "error")
            return redirect(url_for('BP.savings'))

        if action == 'save':
            if budget.curr_total_budget >= amount:
                budget.curr_total_budget -= amount
                savings.curr_savings += amount

                new_txn = SavingsTransaction(
                    savings_id=savings.id,
                    action='save',
                    amount=amount,
                    detail=detail,
                    date=date
                )
                db.session.add(new_txn)
                db.session.commit()
                flash("Money saved successfully!", "success")
            else:
                flash("Insufficient total budget to save this amount.", "error")

        elif action == 'spend':
            category = request.form.get('category')

            # Map categories to their respective models and fields
            category_map = {
                'Accommodation and Utilities': ('accommodation', 'acc_current'),
                'Entertainment': ('entertainment', 'ent_current'),
                'Food': ('food', 'food_current'),
                'Transportation': ('transportation', 'trs_current'),
                'Subscription': ('subscription', 'subs_current'),
                'Others': ('other', 'other_current'),
            }

            if category not in category_map:
                flash("Invalid category selected.", "error")
                return redirect(url_for('BP.savings'))

            rel_name, current_attr = category_map[category]
            category_obj = getattr(budget, rel_name)

            # Create category record if it doesn't exist
            if not category_obj:
                if rel_name == 'accommodation':
                    category_obj = Accommodation(acc_budget=0, acc_current=0)
                elif rel_name == 'entertainment':
                    category_obj = Entertainment(ent_budget=0, ent_current=0)
                elif rel_name == 'food':
                    category_obj = Food(food_budget=0, food_current=0)
                elif rel_name == 'transportation':
                    category_obj = Transportation(trs_budget=0, trs_current=0)
                elif rel_name == 'subscription':
                    category_obj = Subscription(subs_budget=0, subs_current=0)
                elif rel_name == 'other':
                    category_obj = Other(other_budget=0, other_current=0)
                
                db.session.add(category_obj)
                db.session.flush()  # Get the ID
                setattr(budget, f"{rel_name}_id", getattr(category_obj, f"{rel_name}_id"))
                setattr(budget, rel_name, category_obj)

            # Check if total budget has enough funds
            if budget.curr_total_budget >= amount:
                # Deduct from total budget
                budget.curr_total_budget -= amount
                
                # Add to category spending (track as positive)
                current_value = getattr(category_obj, current_attr)
                setattr(category_obj, current_attr, current_value + amount)
                
                # Update category transaction details
                category_obj.transaction = f"Spent {amount}"
                category_obj.detail = detail
                category_obj.date = date

                # Record savings transaction
                new_txn = SavingsTransaction(
                    savings_id=savings.id,
                    action='spend',
                    amount=amount,
                    detail=f"{category}: {detail}" if detail else category,
                    date=date
                )
                db.session.add(new_txn)
                db.session.commit()
                flash("Money spent successfully!", "success")
            else:
                flash("Insufficient total budget.", "error")

        return redirect(url_for('BP.savings'))

    transactions = SavingsTransaction.query.filter_by(savings_id=savings.id).order_by(SavingsTransaction.date.desc()).all() if savings else []

    return render_template(
        'savings.html',
        savings=savings,
        curr_savings=savings.curr_savings if savings else 0,
        saving_goal=savings.saving_goal if savings and savings.saving_goal else 0,
        transactions=transactions,
        budget=budget
    )

@BP.route('/undo_transaction/<int:txn_id>', methods=['POST'])
@login_required_manual
def undo_transaction(txn_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    txn = SavingsTransaction.query.get(txn_id)
    if not txn or txn.savings_id != user.savings_id:
        flash("Invalid transaction.", "error")
        return redirect(url_for('BP.savings'))

    savings = Savings.query.get(user.savings_id)
    budget = user.budget

    if txn.action == 'save':
        if savings.curr_savings >= txn.amount:
            savings.curr_savings -= txn.amount
            budget.curr_total_budget += txn.amount
        else:
            flash("Cannot undo this transaction due to inconsistent data.", "error")
            return redirect(url_for('BP.savings'))

    elif txn.action == 'spend':
        category_map = {
            'Accommodation and Utilities': ('accommodation', 'acc_current'),
            'Entertainment': ('entertainment', 'ent_current'),
            'Food': ('food', 'food_current'),
            'Transportation': ('transportation', 'trs_current'),
            'Subscription': ('subscription', 'subs_current'),
            'Others': ('other', 'other_current'),
        }

        category_name = None
        if txn.detail:
            for cat in category_map.keys():
                if cat in txn.detail:
                    category_name = cat
                    break

        if not category_name:
            flash("Cannot determine category for undo.", "error")
            return redirect(url_for('BP.savings'))

        rel_name, current_attr = category_map[category_name]
        category_obj = getattr(budget, rel_name)
        if not category_obj:
            flash("Category data missing for undo.", "error")
            return redirect(url_for('BP.savings'))

        current_value = getattr(category_obj, current_attr)
        if current_value >= txn.amount:
            setattr(category_obj, current_attr, current_value - txn.amount)
            budget.curr_total_budget += txn.amount
        else:
            flash("Cannot undo this transaction due to inconsistent data.", "error")
            return redirect(url_for('BP.savings'))

    # Delete the transaction (undo)
    db.session.delete(txn)
    db.session.commit()

    flash("Transaction undone successfully.", "success")
    return redirect(url_for('BP.savings'))

@BP.route('/run-monthly-update')
def run_monthly_update():
    from scheduler import perform_monthly_updates
    perform_monthly_updates()
    return "Monthly update performed!"
