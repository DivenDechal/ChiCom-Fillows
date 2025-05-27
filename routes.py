from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime
from models import Savings, db

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
    return render_template('budget.html')


@BP.route('/saving')
def saving():
    if 'user_id' not in session:
        return redirect(url_for('BP.login'))
    return render_template('Saving.html')
    
@BP.route('/savings', methods = [ 'GET', 'POST'])
def savings() :
    if 'user_id' not in session:
        return redirect(url_for('BP.login'))

    if request.method == 'POST':
        try:
            curr_savings = float(request.form.get("amount")
            transaction = request.form.get("transactionType")
            date = datetime.now(tz = "id")
            detail = request.form.get("category")
            print(curr_savings, transaction,date, detail)
            


            add_transaction = Savings(
                curr_savings = curr_savings,
                transaction = transaction,
                detail = detail,
                date = date
            )

            db.session.add(add_transaction)
            db.session.commit()
            print("new transaction added!")
            return render_template('savings.html)
            

        except Exception as e:
            print("error add transaction")
            return "error add transaction"

    else:
        return render_template('savings.html')
    
    
