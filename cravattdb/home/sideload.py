"""Helper methods for creating datasets."""
from cravattdb import app
from zipfile import ZipFile
import cravattdb.api.api as api
import pathlib


def sideload_experiment(data, user_id, file):
    data.update({'user_id': user_id})
    experiment = api.add_experiment(data)
    experiment_id = experiment['id']

    cimage_data_path = _unzip_cimage(file, user_id, experiment_id)

    dta_path = list(cimage_data_path.glob('dta*'))[0]

    output_file_path = pathlib.Path(
        cimage_data_path,
        dta_path,
        'output',
        'output_rt_10_sn_2.5.to_excel.txt'
    )

    api.add_dataset(experiment_id, int(user_id), output_file_path)

    return experiment


def _unzip_cimage(file, user_id, dataset_id):
    extract_path = pathlib.Path(
        app.instance_path,
        'legacy',
        str(user_id),
        str(dataset_id)
    )

    with ZipFile(file, 'r') as cimage_zip:
        cimage_zip.extractall(str(extract_path))

    return extract_path
