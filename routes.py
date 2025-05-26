from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models import db, User, Budget, Account, Entertainment, Food, Transportation, Subscription, Other, SavingsTransaction, Savings
from datetime import datetime

BP = Blueprint('BP', __name__)

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
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('BP.login'))

    user = User.query.get(user_id)
    if not user or not user.budget_id:
        return redirect(url_for('BP.savings'))

    budget = Budget.query.get(user.budget_id)
    if not budget:
        flash("Budget not found.", "error")
        return redirect(url_for('BP.savings'))

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
    category_values = [cat["budget"] or 0 for cat in categories.values()]

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

@BP.route('/savings')
def savings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('BP.login'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('BP.login'))

    saving_goal = (user.income or 0) * ((user.splitting or 0) / 100)

    # Create or retrieve savings account
    savings = Savings.query.get(user.savings_id) if user.savings_id else None
    if not savings:
        savings = Savings(curr_savings=0.0)
        db.session.add(savings)
        db.session.commit()
        user.savings_id = savings.id
        db.session.commit()

    transactions = SavingsTransaction.query.filter_by(savings_id=savings.id)\
                                           .order_by(SavingsTransaction.date.desc())\
                                           .all()

    return render_template(
        'savings.html',
        curr_savings=savings.curr_savings,
        saving_goal=saving_goal,
        transactions=transactions
    )

@BP.route('/savings/transaction', methods=['POST'])
def savings_transaction():
    user_id = session.get('user_id')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not user_id:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Session expired'}), 401
        return redirect(url_for('BP.login'))

    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")

        # Get or create savings account
        savings = Savings.query.get(user.savings_id) if user.savings_id else None
        if not savings:
            savings = Savings(curr_savings=0.0)
            db.session.add(savings)
            db.session.commit()
            user.savings_id = savings.id
            db.session.commit()

        # Parse form data
        amount = float(request.form.get('amount', 0))
        action = request.form.get('action')
        category = request.form.get('category') or "Others"
        detail = request.form.get('detail', '')

        # Validate form input
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if action not in ['save', 'spend']:
            raise ValueError("Invalid transaction type")

        if action == 'spend':
            if savings.curr_savings < amount:
                raise ValueError("Insufficient savings")

            if not user.budget_id:
                raise ValueError("No budget configured - please set up your budget first")

            budget = Budget.query.get(user.budget_id)
            if not budget:
                raise ValueError("Budget not found")

            # Ensure related budget category objects exist
            if category == "Accommodation and Utilities":
                if not budget.account:
                    budget.account = Account(acc_budget=0.0, acc_current=0.0)
                    db.session.add(budget.account)
                budget.account.acc_current += amount
                budget.account.transaction = detail
                budget.account.date = datetime.utcnow()

            elif category == "Entertainment":
                if not budget.entertainment:
                    budget.entertainment = Entertainment(ent_budget=0.0, ent_current=0.0)
                    db.session.add(budget.entertainment)
                budget.entertainment.ent_current += amount
                budget.entertainment.transaction = detail
                budget.entertainment.date = datetime.utcnow()

            elif category == "Food and Clothes":
                if not budget.food:
                    budget.food = Food(food_budget=0.0, food_current=0.0)
                    db.session.add(budget.food)
                budget.food.food_current += amount
                budget.food.transaction = detail
                budget.food.date = datetime.utcnow()

            elif category == "Transportation":
                if not budget.transportation:
                    budget.transportation = Transportation(trs_budget=0.0, trs_current=0.0)
                    db.session.add(budget.transportation)
                budget.transportation.trs_current += amount
                budget.transportation.transaction = detail
                budget.transportation.date = datetime.utcnow()

            elif category == "Subscription":
                if not budget.subscription:
                    budget.subscription = Subscription(subs_budget=0.0, subs_current=0.0)
                    db.session.add(budget.subscription)
                budget.subscription.subs_current += amount
                budget.subscription.transaction = detail
                budget.subscription.date = datetime.utcnow()

            elif category == "Others":
                if not budget.other:
                    budget.other = Other(other_budget=0.0, other_current=0.0)
                    db.session.add(budget.other)
                budget.other.other_current += amount
                budget.other.transaction = detail
                budget.other.date = datetime.utcnow()

        # Update savings balance
        savings.curr_savings += amount if action == 'save' else -amount
        savings.transaction = detail
        savings.date = datetime.utcnow()

        # Record savings transaction
        txn = SavingsTransaction(
            savings_id=savings.id,
            action=action,
            amount=amount,
            category=category,
            detail=detail,
            date=datetime.utcnow()
        )
        db.session.add(txn)
        db.session.commit()

        if is_ajax:
            return jsonify({
                'success': True,
                'currentSavings': savings.curr_savings,
                'message': f"{'Saved' if action == 'save' else 'Spent'} Rp {amount:,.2f} in {category}"
            })

        return redirect(url_for('BP.savings'))

    except Exception as e:
        db.session.rollback()
        if is_ajax:
            return jsonify({'success': False, 'message': str(e)}), 400
        flash(f"Transaction failed: {str(e)}", "error")
        return redirect(url_for('BP.savings'))
