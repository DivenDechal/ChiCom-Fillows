from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User, SavingsTransaction

def perform_monthly_updates():
    print("Running scheduled monthly update...")
    users = User.query.all()

    for user in users:
        if not user.savings or not user.budget:
            continue  # Skip if data is incomplete

        # Split income into savings and budget parts
        income = user.income
        split_ratio = user.splitting / 100.0
        savings_amount = income * split_ratio
        budget_amount = income * (1 - split_ratio)

        # Update savings and savings goal
        user.savings.curr_savings += savings_amount
        if user.savings.saving_goal is not None:
            user.savings.saving_goal += savings_amount

        # Record savings transaction
        db.session.add(SavingsTransaction(
            savings_id=user.savings.id,
            action='save',
            amount=savings_amount,
            detail='Monthly savings contribution',
            date=datetime.utcnow()
        ))

        # Calculate unused budget from all categories
        budget = user.budget
        leftover = budget.curr_total_budget

     #   try:
     #       leftover += budget.accommodation.acc_budget - budget.accommodation.acc_current
     #       leftover += budget.entertainment.ent_budget - budget.entertainment.ent_current
     #       leftover += budget.food.food_budget - budget.food.food_current
     #       leftover += budget.transportation.trs_budget - budget.transportation.trs_current
     #       leftover += budget.subscription.subs_budget - budget.subscription.subs_current
     #       leftover += budget.other.other_budget - budget.other.other_current
     #   except AttributeError:
            # Skip users with incomplete subcategories
     #       continue

        if leftover > 0:
            user.savings.curr_savings += leftover
            db.session.add(SavingsTransaction(
                savings_id=user.savings.id,
                action='save',
                amount=leftover,
                detail='Carryover from unused budget',
                date=datetime.utcnow()
            ))

        # Update total budget
        budget.curr_total_budget = budget_amount

        # Reset current category spending
        budget.accommodation.acc_current = 0
        budget.entertainment.ent_current = 0
        budget.food.food_current = 0
        budget.transportation.trs_current = 0
        budget.subscription.subs_current = 0
        budget.other.other_current = 0

    db.session.commit()
    print("Monthly update completed successfully.")

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: app.app_context().push() or perform_monthly_updates(),
                      trigger='cron', day=1, hour=0, minute=0)
    scheduler.start()
    print("Scheduler started. Monthly updates will run on the 1st of each month.")
