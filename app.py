from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning


# Import and Register the blueprint
from routes import BP
app.register_blueprint(BP)

db.init_app(app)

@app.cli.command()
def initdb():
    with app.app_context():
        db.create_all()
    print("Database created!")

if __name__ == '__main__':
    app.run(debug=True)
