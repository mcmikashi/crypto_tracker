"""Flask configuration."""
from os import environ, path, urandom
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_TIMEZONE = "Europe/Paris"


class DevConfig(Config):
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")


class TestConfig(Config):
    SECRET_KEY = urandom(16).hex()
    SQLALCHEMY_DATABASE_URI = environ.get("TEST_DATABASE_URI")
    TESTING = True
    LOGIN_DISABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False
