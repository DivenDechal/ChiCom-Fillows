from flask import Flask
from models import db
from auth import BP_auth
from routes import BP  # Ensure this exists and doesn't cause import error

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(BP)  # Make sure this blueprint is defined correctly
    app.register_blueprint(BP_auth, url_prefix='/auth')

    # CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        with app.app_context():
            db.create_all()
            print("Database initialized!")

    return app

# For running directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

