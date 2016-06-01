"""Blueprint for users."""
from flask import Blueprint
from cravattdb import db

users = Blueprint('users', __name__,
                  template_folder='templates',
                  static_folder='static')


@users.before_app_first_request
def create_user():
    db.create_all()
    db.session.commit()
