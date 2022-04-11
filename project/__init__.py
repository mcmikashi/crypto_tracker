from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "authentification.login"


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    login_manager.init_app(app)
    from .authentification.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our
        # user table, use it in the query for the user
        return User.query.get(int(user_id))


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    # blueprint for auth routes in our app

    # Add authentification
    from project.authentification import authentification_blueprint

    app.register_blueprint(authentification_blueprint)

    # Add cryptocurrency
    from project.cryptocurrency import cryptocurrency_blueprint

    app.register_blueprint(cryptocurrency_blueprint)
