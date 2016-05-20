"""Blueprint for front-end."""

from flask import Blueprint, render_template
from flask.ext.security import login_required
from flask_security.core import current_user
import cravattdb.models.api as api

home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
@login_required
def index():
    meta = current_user.meta
    return render_template('index.html', meta=meta, id=current_user.email)


@home.route('/sideload')
@login_required
def sideload_dataset():
    bootstrap = {
        **api.get_organism(),
        **api.get_probe(),
        **api.get_inhibitor(),
        **api.get_experiment_type()
    }

    return render_template('index.html', bootstrap=bootstrap)


@home.route('/experiments')
@login_required
def render_experiments():
    bootstrap = api.get_experiment(flat=True)
    return render_template('index.html', bootstrap={'experiments': bootstrap})


@home.route('/experiment/<int:experiment_id>')
@login_required
def render_experiment(experiment_id):
    raw = api.get_dataset(experiment_id)

    return render_template('index.html', bootstrap={
        'experiment': {
            'data': [list(item.values()) for item in raw['dataset']],
            'id': experiment_id
        }
    })
