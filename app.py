from flask import Flask
from models import db
from routes import BP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(BP)

db.init_app(app)

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
    print("Database initialized!")

if __name__ == '__main__':
    app.run(debug=True)
