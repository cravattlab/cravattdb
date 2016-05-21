"""Blueprint for legacy thangs."""

from flask import Blueprint, send_from_directory
from cravattdb import app
from pathlib import Path
import math

legacy = Blueprint('legacy', __name__,
                   template_folder='templates',
                   static_folder='static')


@legacy.route('/<int:user_id>/<int:experiment_id>')
def render_dataset(user_id, experiment_id):
    dataset_path = _get_dataset_path(user_id, experiment_id)
    return send_from_directory(dataset_path, 'combined_dta.html')


@legacy.route('/<int:user_id>/<int:experiment_id>/chromatogram/<int:chromatogram_index>')
def render_chromatogram(user_id, experiment_id, chromatogram_index):
    dataset_path = _get_dataset_path(user_id, experiment_id)

    group = math.floor((chromatogram_index - 1) / 500)
    corrected_index = (chromatogram_index - 1) % 500

    chromatogram_path = Path(
        dataset_path,
        'dta',
        'output',
        'PNG',
        str(group)
    )

    chromatogram_file_name = 'output_rt_10_sn_2.5.{}_{}.png'.format(group, corrected_index)
    return send_from_directory(str(chromatogram_path), chromatogram_file_name)


def _get_dataset_path(user_id, experiment_id):
    path_to_legacy = Path(
        app.instance_path,
        'legacy',
        str(user_id),
        str(experiment_id)
    )

    return str(path_to_legacy)
