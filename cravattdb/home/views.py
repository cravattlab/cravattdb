"""Blueprint for front-end."""

from flask import Blueprint, render_template, make_response, jsonify
from flask_security import current_user, login_required, LoginForm
from http import HTTPStatus

home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
@home.route('/search')
@home.route('/search<string:matrix>')
@login_required
def index(matrix=None):
    meta = current_user.meta
    return render_template('index.html', meta=meta, id=current_user.email)


@home.route('/user_id')
@login_required
def get_user_id():
    return current_user.get_id()


@home.route('/experiments')
@login_required
def render_experiments():
    return render_template('index.html')


@home.route('/probes')
@login_required
def render_probes():
    return render_template('index.html')


@home.route('/experiment/<int:experiment_id>')
@login_required
def render_experiment(experiment_id):
    return render_template('index.html')


@home.route('/login_csrf')
def login_csrf():
    form = LoginForm()
    return jsonify({'csrf_token': form.csrf_token.current_token})


@home.app_errorhandler(HTTPStatus.CONFLICT)
def dataset_exists(error):
    return make_response(jsonify({'error': error.description}), error.code)
