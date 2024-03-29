"""Backend for a proteomics database."""
from flask import Flask, jsonify, make_response
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_mail import Mail
from flask_admin import Admin
from flask_migrate import Migrate
from .contrib.ldap import LDAPUserDatastore, LDAPLoginForm
from .utils.converters import MatrixConverter
from .utils.admin import AuthAdminIndexView
import config.config as config


# setup da app
app = Flask(__name__, instance_path=str(config.INSTANCE_PATH))
app.config.from_object(config.config)
mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)

# Setup Flask-Migrate
migrate = Migrate(app, db, directory='cravattdb/migrations')

# Setup Flask-Admin
from .admin.views import bootstrap_admin
admin = Admin(app,
              name=config.PROJECT_NAME,
              template_mode='bootstrap3',
              index_view=AuthAdminIndexView())
bootstrap_admin(admin, db)

"""
We register blue prints after setting up app and db so that we can import these
when needed. From the Flask gods themselves regarding circular imports:

Every Python programmer hates them, and yet we just added some: circular imports
(That’s when two modules depend on each other. In this case views.py depends on
__init__.py). Be advised that this is a bad idea in general but here it is actually
 fine. The reason for this is that we are not actually using the views in __init__.py
  and just ensuring the module is imported and we are doing that at the bottom of the file.
"""

# Setup Flask-Security with LDAP goodness
from .users.models import User, Role
user_datastore = LDAPUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=LDAPLoginForm)

# url converter for matrix parameters. Used by Angular2 and convenient to have
# server-side as well
app.url_map.converters['matrix'] = MatrixConverter

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
