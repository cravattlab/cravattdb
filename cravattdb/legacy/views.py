"""Blueprint for legacy thangs."""

from flask import Blueprint, send_from_directory
from cravattdb import app
from pathlib import Path

legacy = Blueprint('legacy', __name__,
                   template_folder='templates',
                   static_folder='static')


@legacy.route('/<int:user_id>/<int:experiment_id>')
def render_dataset(user_id, experiment_id):
    path_to_legacy = Path(
        app.instance_path,
        'legacy',
        str(user_id),
        str(experiment_id)
    )

    return send_from_directory(str(path_to_legacy), 'combined_dta.html')
