"""Backend for a proteomics database."""
from flask import Flask, jsonify, make_response
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_admin import Admin
from http import HTTPStatus
import config.config as config
import os

instance_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    config.UPLOAD_FOLDER
)

# setup da app
app = Flask(__name__, instance_path=instance_path)
app.config.from_object(config.DevelopmentConfig)
mail = Mail(app)

# Create database connection object
db = SQLAlchemy()
db.init_app(app)

"""
We register blue prints after setting up app and db so that we can import these
when needed. From the Flask gods themselves regarding circular imports:

Every Python programmer hates them, and yet we just added some: circular imports
(That’s when two modules depend on each other. In this case views.py depends on
__init__.py). Be advised that this is a bad idea in general but here it is actually
 fine. The reason for this is that we are not actually using the views in __init__.py
  and just ensuring the module is imported and we are doing that at the bottom of the file.
"""

# Setup Flask-Security
from .users.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Setup Flask-Admin
admin = Admin(app, name='cravattdb', template_mode='bootstrap3')

# get da blueprints
from .home.views import home
from .auto.views import auto
from .users.views import users
from .api.views import api
from .legacy.views import legacy

app.register_blueprint(home)
app.register_blueprint(auto, url_prefix='/auto')
app.register_blueprint(users)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(legacy, url_prefix='/legacy')


@app.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized(error):
    return make_response(jsonify({'error': error.description}), error.code)
