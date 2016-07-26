"""Helper methods for creating datasets."""
from cravattdb import app
from zipfile import ZipFile
import cravattdb.api.api as api
import pathlib


def sideload_experiment(data, user_id, file):
    data['user_id'] = user_id
    treatment_data = data.pop('treatment')

    experiment = api.add_experiment(data)
    experiment_id = experiment['id']

    load_treatment(experiment_id, treatment_data)
    load_data(user_id, experiment_id, file)

    return experiment


def load_treatment(experiment_id, treatment_data):
    for fraction, fraction_data in treatment_data.items():
        for item, data in fraction_data.items():
            data.update({
                'experiment_id': experiment_id,
                'fraction': fraction,
                '{}_id'.format(item): data.pop('id')
            })
            api.add_treatment(data)


def load_data(user_id, experiment_id, file):
    cimage_data_path = _unzip_cimage(file, user_id, experiment_id)

    dta_path = list(cimage_data_path.glob('dta*'))[0]

    output_file_path = pathlib.Path(
        cimage_data_path,
        dta_path,
        'output',
        'output_rt_10_sn_2.5.to_excel.txt'
    )

    api.add_dataset(experiment_id, int(user_id), output_file_path)


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
