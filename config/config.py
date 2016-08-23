"""ONLY (kind of :/) configuration file for project."""

import yaml
import os
import pathlib


# debug is true by default
DEBUG = bool(os.getenv('DEBUG', True))
_secrets_path = 'config/secrets{}.yml'.format('' if DEBUG else '.prod')
_override_path = 'config/secrets.override.yml'

# get our secrets
with open(_secrets_path, 'r') as f:
    _SECRETS = yaml.load(f)

# provide a mechanism for overriding some secrets
if os.path.isfile(_override_path):
    with open(_override_path, 'r') as f:
        _SECRETS.update(yaml.load(f))

# remove extraneous 'environment' wrapper without which docker-compose will bitch
# this is only necessary to avoid duplication of secrets
_SECRETS = {k: v['environment'] for k, v in _SECRETS.items()}

PROJECT_NAME = 'cravattdb'
PROJECT_HOME_PATH = pathlib.PurePath(os.path.realpath(__file__)).parents[1]
SEARCH_PARAMS_PATH = PROJECT_HOME_PATH.joinpath(PROJECT_NAME, 'auto', 'search_params')
INSTANCE_PATH = PROJECT_HOME_PATH.joinpath(PROJECT_NAME, 'uploads')

CONVERT_URL = 'http://cravattwork.scripps.edu:5001'


class _Config(object):
    """Holds flask configuration to be consumed by Flask's from_object method."""

    # Flask
    DEBUG = False
    SECRET_KEY = _SECRETS['flask']['SECRET_KEY']
    JSONIFY_PRETTYPRINT_REGULAR = False

    # Flask-Security
    SECURITY_PASSWORD_SALT = _SECRETS['flask-security']['SECURITY_PASSWORD_SALT']
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = ''
    EMAIL = _SECRETS['mail']['EMAIL']
    EMAIL_PASSWORD = _SECRETS['mail']['EMAIL_PASSWORD']

    # LDAP configuration
    SECURITY_LDAP_URI = 'ldap://lj.ad.scripps.edu'
    SECURITY_LDAP_BASE_DN = 'OU=Research Divisions,DC=lj,DC=ad,DC=scripps,DC=edu'
    SECURITY_LDAP_SEARCH_FILTER = 'sAMAccountName={}'
    SECURITY_LDAP_BIND_DN = _SECRETS['flask-security']['SECURITY_LDAP_BIND_DN']
    SECURITY_LDAP_BIND_PASSWORD = _SECRETS['flask-security']['SECURITY_LDAP_BIND_PASSWORD']
    SECURITY_LDAP_EMAIL_FIELDNAME = 'mail'
    SECURITY_MSG_USERID_NOT_PROVIDED = ('User ID not provided', 'error')
    SECURITY_MSG_LDAP_SERVER_DOWN = ("""The Scripps authentication server is down or not accessible, please try the
                                            last password you successfully used to login to this server.""", 'error')
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['email', 'username']

    # Flask-SqlAlchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@postgres/{}'.format(
        _SECRETS['database']['DB_USER'],
        _SECRETS['database']['DB_PASS'],
        _SECRETS['database']['DB_NAME']
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _DevelopmentConfig(_Config):
    """Configuration for development environment."""

    DEBUG = True


config = _DevelopmentConfig if DEBUG else _Config
