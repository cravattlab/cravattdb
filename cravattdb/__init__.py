"""Backend for a proteomics database."""
from flask import Flask, jsonify, make_response
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from cravattdb.models.database import db, User, Role
from http import HTTPStatus
from .home.views import home
from .api.views import api
from .auto.views import auto
import config.config as config
import os

instance_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    config.UPLOAD_FOLDER
)

app = Flask(__name__, instance_path=instance_path)

app.register_blueprint(home)
app.register_blueprint(auto)
app.register_blueprint(api, url_prefix='/api')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECURITY_REGISTERABLE'] = True
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.EMAIL
app.config['MAIL_PASSWORD'] = config.EMAIL_PASSWORD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


mail = Mail(app)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    db.create_all()
    db.session.commit()


def error_response(details, code):
    return make_response(jsonify({'error': details}), code)


@app.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized(error):
    return error_response(error.description, error.code)


@app.errorhandler(HTTPStatus.CONFLICT)
def dataset_exists(error):
    return error_response(error.description, error.code)
