from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models import db, User, Budget, Accommodation, Entertainment, Food, Transportation, Subscription, Other, SavingsTransaction, Savings, BudgetTransaction, Loan
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

@BP.route('/budget', methods=['GET', 'POST'])
@login_required_manual
def budget():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    # Ensure the user has a budget object and associated categories
    if not user.budget:
        budget = Budget(curr_total_budget=user.income or 0)

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

    if request.method == 'POST':
        category = request.form.get('category')
        cost = float(request.form.get('cost', 0))
        detail = request.form.get('detail', '')
        now = datetime.now()

        if cost <= 0:
            flash("Invalid transaction amount.", "error")
            return redirect(url_for('BP.budget'))

        if budget.curr_total_budget < cost:
            flash("Insufficient total budget to add this transaction.", "error")
            return redirect(url_for('BP.budget'))

        transaction = BudgetTransaction(
            user_id=user.id,
            category=category,
            amount=cost,
            detail=detail,
            date=now
        )
        db.session.add(transaction)

        if category == 'accommodation' and budget.accommodation:
            budget.accommodation.acc_current += cost
            budget.accommodation.transaction = detail
            budget.accommodation.date = now
            budget.accommodation.detail = detail
        elif category == 'entertainment' and budget.entertainment:
            budget.entertainment.ent_current += cost
            budget.entertainment.transaction = detail
            budget.entertainment.date = now
            budget.entertainment.detail = detail
        elif category == 'food' and budget.food:
            budget.food.food_current += cost
            budget.food.transaction = detail
            budget.food.date = now
            budget.food.detail = detail
        elif category == 'transportation' and budget.transportation:
            budget.transportation.trs_current += cost
            budget.transportation.transaction = detail
            budget.transportation.date = now
            budget.transportation.detail = detail
        elif category == 'subscription' and budget.subscription:
            budget.subscription.subs_current += cost
            budget.subscription.transaction = detail
            budget.subscription.date = now
            budget.subscription.detail = detail
        elif category == 'others' and budget.other:
            budget.other.other_current += cost
            budget.other.transaction = detail
            budget.other.date = now
            budget.other.detail = detail
        else:
            return "Invalid category", 400

        # Deduct total budget for the transaction cost
        budget.curr_total_budget -= cost

        db.session.commit()
        flash("Transaction added successfully!", "success")
        return redirect(url_for('BP.budget'))

    # Prepare category data for chart and rendering
    categories = {
        "Accommodation and Utilities": {
            "budget": budget.accommodation.acc_budget if budget.accommodation else 0,
            "current": budget.accommodation.acc_current if budget.accommodation else 0,
            "key": "accommodation"
        },
        "Entertainment": {
            "budget": budget.entertainment.ent_budget if budget.entertainment else 0,
            "current": budget.entertainment.ent_current if budget.entertainment else 0,
            "key": "entertainment"
        },
        "Food and Clothes": {
            "budget": budget.food.food_budget if budget.food else 0,
            "current": budget.food.food_current if budget.food else 0,
            "key": "food"
        },
        "Transportation": {
            "budget": budget.transportation.trs_budget if budget.transportation else 0,
            "current": budget.transportation.trs_current if budget.transportation else 0,
            "key": "transportation"
        },
        "Subscription": {
            "budget": budget.subscription.subs_budget if budget.subscription else 0,
            "current": budget.subscription.subs_current if budget.subscription else 0,
            "key": "subscription"
        },
        "Others": {
            "budget": budget.other.other_budget if budget.other else 0,
            "current": budget.other.other_current if budget.other else 0,
            "key": "others"
        }
    }

    category_labels = list(categories.keys())
    category_values = [cat["current"] or 0 for cat in categories.values()]

    if not any(category_values):
        category_labels = ["No Data"]
        category_values = [1]

    # Group all budget transactions by category for modal display
    budget_transactions = BudgetTransaction.query.filter_by(user_id=user.id).order_by(BudgetTransaction.date.desc()).all()
    transactions_by_category = {}
    for txn in budget_transactions:
        transactions_by_category.setdefault(txn.category, []).append(txn)

    return render_template(
        'budget.html',
        total_budget=budget.curr_total_budget or 0,
        categories=categories,
        category_labels=category_labels,
        category_values=category_values,
        transactions_by_category=transactions_by_category
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
            

        elif action == 'spend':
            category = request.form.get('category')

            if amount <= 0:
                flash("Amount must be greater than zero.", "error")
                return redirect(url_for('BP.savings'))
            
            if savings.curr_savings >= amount:
                # Deduct from savings
                savings.curr_savings -= amount

                # Record savings transaction (category included in detail only)
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
                flash("Insufficient savings balance.", "error")

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
        # Check if we can undo spending safely
        if current_value >= txn.amount and savings.curr_savings + txn.amount >= 0:
            setattr(category_obj, current_attr, current_value - txn.amount)
            savings.curr_savings += txn.amount  # Return money back to savings, not budget
        else:
            flash("Cannot undo this transaction due to inconsistent data.", "error")
            return redirect(url_for('BP.savings'))

    # Delete the transaction (undo)
    db.session.delete(txn)
    db.session.commit()

    flash("Transaction undone successfully.", "success")
    return redirect(url_for('BP.savings'))


# Add this to your BP file

@BP.route('/account', methods=['GET'])
@login_required_manual
def account():
    user = get_current_user()
    return render_template('account.html', user=user)

@BP.route('/update_profile', methods=['POST'])
@login_required_manual
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify(success=False, message="Not logged in"), 401

    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.income = float(data.get('income', user.income))
    user.splitting = int(data.get('savingRatio', user.splitting))  # match naming!

    db.session.commit()
    return jsonify(success=True, message="Profile updated successfully!")


@BP.route('/change_password', methods=['POST'])
@login_required_manual
def change_password():
    user = get_current_user()
    if not user:
        return jsonify(success=False, message="Not logged in"), 401

    data = request.json
    new_password = data.get('newPassword')
    if new_password:
        user.set_password(new_password)  # ✅ hash it properly!
        db.session.commit()
        return jsonify(success=True, message="Password changed successfully!")
    return jsonify(success=False, message="Password is required")


@BP.route('/delete_account', methods=['POST'])
@login_required_manual
def delete_account():
    user = get_current_user()
    confirmation = request.json.get('confirmation')
    if confirmation == 'DELETE':
        # In real app: flag for deletion instead of immediate delete
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return jsonify(success=True, message="Your account has been deleted.")
    return jsonify(success=False, message="Invalid confirmation.")


@BP.route('/logout')
@login_required_manual
def logout():
    flash('Successfully logged out', 'success')
    session.pop('user_id', None)
    return redirect(url_for('BP.login'))

@BP.route('/debts', methods=['GET'])
@login_required_manual
def debts():
    user = get_current_user()
    if not user:
        return redirect(url_for('BP.login'))

    debts = Loan.query.filter_by(user_id=user.id).order_by(Loan.date_added.desc()).all()

    # Serialize loans to dictionaries
    serialized_debts = []
    for loan in debts:
        serialized_debts.append({
            'id': loan.id,
            'amount': loan.amount,
            'interest_rate': loan.interest_rate,
            'details': loan.details,
            'date_added': loan.date_added.strftime("%Y-%m-%d %H:%M:%S")
        })

    return render_template('debts.html', debts=serialized_debts)



@BP.route('/debts/add', methods=['POST'])
@login_required_manual
def add_debt():
    user = get_current_user()
    if not user:
        return jsonify(success=False, message="Not logged in"), 401

    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        interest_rate = float(data.get('interest_rate', 0))
        details = data.get('details', '').strip()

        if amount <= 0:
            return jsonify(success=False, message="Loan amount must be greater than zero.")

        new_loan = Loan(
            user_id=user.id,
            amount=amount,
            interest_rate=interest_rate,
            details=details,
            date_added=datetime.now()
        )
        db.session.add(new_loan)
        db.session.commit()

        return jsonify(success=True, message="Loan added successfully.")

    except Exception as e:
        return jsonify(success=False, message=str(e)), 400


@BP.route('/debts/delete/<int:loan_id>', methods=['DELETE'])
@login_required_manual
def delete_debt(loan_id):
    user = get_current_user()
    if not user:
        return jsonify(success=False, message="Not logged in"), 401

    loan = Loan.query.filter_by(id=loan_id, user_id=user.id).first()
    if not loan:
        return jsonify(success=False, message="Loan not found.")

    db.session.delete(loan)
    db.session.commit()

    return jsonify(success=True, message="Loan deleted successfully.")


@BP.route('/run-monthly-update')
def run_monthly_update():
    from scheduler import perform_monthly_updates
    perform_monthly_updates()
    return "Monthly update performed!"

