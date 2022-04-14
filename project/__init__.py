from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
# init the LoginManager instance
login_manager = LoginManager()
login_manager.login_view = "authentification.login"
# Set the message if user tries to go on a page that require to be logged
login_manager.login_message = "Vous devez être connecté pour voir cette page"
login_manager.login_message_category = "warning"
# init APScheduler instance
scheduler = APScheduler()


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    # initialize the database with the app
    db.init_app(app)
    # initialize APScheduler with the app
    scheduler.init_app(app)
    from project.cryptocurrency.utils import \
        update_quote, daily_update_user_last_valorization

    # Every 5 minutes get the last quote currency of
    # all cryptorency that is on the database
    @scheduler.task("interval", id="update_last_quote", minutes=5)
    def update_last_quote():
        with app.app_context():
            update_quote()

    # Every day at 00:01  we get the last yesterday
    # profit of all user and store it to the database
    @scheduler.task("cron", id="add_all_user_profit", hour=0, minute=1)
    def update_all_user_valorisation():
        with app.app_context():
            daily_update_user_last_valorization()

    if app.config["FLASK_ENV"] != "development":
        scheduler.start()

    # initialize Login Manager with the app
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
