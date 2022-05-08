"""Flask configuration."""
from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_TIMEZONE = "UTC"
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get("EMAIL")
    MAIL_PASSWORD = environ.get("EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = environ.get("EMAIL")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    MAIL_DEBUG = True
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")


class TestConfig(Config):
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URI")
    TESTING = True
    DEBUG = True
    LOGIN_DISABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False


class Prodconfig(Config):
    FLASK_ENV = "production"
    uri = environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri
