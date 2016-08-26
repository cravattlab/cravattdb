"""Blueprint for legacy thangs."""

from flask import Blueprint, send_from_directory
from flask_autoindex import AutoIndexBlueprint
from pathlib import Path
import config.config as config
import math

legacy = Blueprint('legacy', __name__,
                   template_folder='templates',
                   static_folder='static')

AutoIndexBlueprint(legacy, browse_root=str(config.INSTANCE_PATH.joinpath('legacy')))


@legacy.route('/<int:user_id>/<int:experiment_id>/chromatogram/<int:chromatogram_index>')
def render_chromatogram(user_id, experiment_id, chromatogram_index):
    dataset_path = _get_dataset_path(user_id, experiment_id)

    group = math.floor((chromatogram_index - 1) / 500)
    corrected_index = (chromatogram_index - 1) % 500

    if dataset_path.joinpath('dta').exists():
        dta_folder = 'dta'
    else:
        dta_folder = 'dta_HL'

    chromatogram_path = dataset_path.joinpath(
        dta_folder,
        'output',
        'PNG',
        str(group)
    )

    chromatogram_file_name = 'output_rt_10_sn_2.5.{}_{}.png'.format(group, corrected_index)
    return send_from_directory(str(chromatogram_path), chromatogram_file_name)


def _get_dataset_path(user_id, experiment_id):
    path_to_legacy = Path(
        config.INSTANCE_PATH,
        'legacy',
        str(user_id),
        str(experiment_id)
    )

    return path_to_legacy
