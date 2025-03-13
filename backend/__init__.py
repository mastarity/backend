from flask import Flask
from backend.models import db
from flask_jwt_extended  import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .auth import auth
from .courses import courses


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['JWT_SECRET_KEY'] = '3tfhryeyrt3454rtrtur' # Change in production

    app.register_blueprint(auth)
    app.register_blueprint(courses)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Create tables
    with app.app_context():
        db.drop_all()  
        db.create_all()

    return app
