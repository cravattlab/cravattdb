"""Main configuration file for project."""
import yaml
import os
import pathlib

# Database settings
with open('config/database.yml', 'r') as f:
    database_settings = yaml.load(f)

PROJECT_NAME = 'cravattdb'
PROJECT_HOME_PATH = pathlib.PurePath(os.path.realpath(__file__)).parents[1]
SEARCH_PARAMS_PATH = PROJECT_HOME_PATH.joinpath(PROJECT_NAME, 'auto', 'search_params')
INSTANCE_PATH = PROJECT_HOME_PATH.joinpath(PROJECT_NAME, 'uploads')

CONVERT_URL = 'http://cravattwork.scripps.edu:5001'


class Config(object):
    """Holds flask configuration."""

    DEBUG = False

    # Flask-Security
    SECRET_KEY = 'super-secret'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    EMAIL = 'mail@example.com'
    EMAIL_PASSWORD = 'password'

    SECURITY_REGISTERABLE = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@postgres/{}'.format(
        database_settings['database']['environment']['DB_USER'],
        database_settings['database']['environment']['DB_PASS'],
        database_settings['database']['environment']['DB_NAME']
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration for development environment."""

    DEBUG = True
