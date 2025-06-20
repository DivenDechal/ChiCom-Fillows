from flask import Flask
from models import db
from auth import BP_auth
from routes import BP
from scheduler import start_scheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(BP)  # Main routes at root
app.register_blueprint(BP_auth, url_prefix='/auth')  # Auth routes under /auth

db.init_app(app)

@app.cli.command("init-db")
def init_db():
    print("Running init-db command...")
    with app.app_context():
        db.create_all()
    print("Database initialized!")

with app.app_context():
    db.create_all()
    start_scheduler(app)

if __name__ == '__main__':
    app.run(debug=True)
