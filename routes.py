from flask import Blueprint, render_template, session, redirect, url_for

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
    return render_template('savings.html')

@BP.route('/account')
def account():
    return render_template('account.html')