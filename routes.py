from flask import Blueprint, render_template, session
BP = Blueprint('BP', __name__)

@BP.route('/')
def home():
    return render_template('main.html', user=session.get('user'))