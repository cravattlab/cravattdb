"""Define processing actions for celery task queue."""
from celery import Celery
from redis import StrictRedis
import cravattdb.auto.convert as convert
import cravattdb.auto.quantify as quantify
import cravattdb.api.api as api
import shutil
import pathlib

celery = Celery('tasks', broker='amqp://guest@rabbitmq//')
redis = StrictRedis(host='redis')


@celery.task
def process(search, user_id, name, path, organism_id, organism_name, experiment_type_id, experiment_type_name, probe_id, inhibitor_id):
    set_status = update_status(user_id, name)
    set_status('converting')

    # convert .raw to .ms2
    # removing first bit of file path since that is the upload folder
    corrected_path = pathlib.PurePath(*path.parts[path.parts.index('processing') + 1:])
    convert_status = convert.convert(corrected_path.as_posix())

    converted_paths = [path.joinpath(f) for f in convert_status['files_converted']]
    set_status('searching ip2')

    # initiate IP2 search
    dta_select_link = search.search(
        organism_name,
        experiment_type_name,
        [f for f in converted_paths if f.suffix == '.ms2']
    )

    set_status('quantification')

    # quantify all of the things
    quantify.quantify(
        name,
        dta_select_link,
        experiment_type_name,
        path
    )

    set_status('loading into database')

    experiment = api.add_experiment(
        name=name,
        user_id=user_id,
        organism_id=organism_id,
        experiment_type_id=experiment_type_id,
        probe_id=probe_id,
        inhibitor_id=inhibitor_id,
    )

    experiment_id = experiment['id']

    # move cimage results to legacy folder, grab file and load into database
    new_path = path.parents[0].joinpath('legacy', user_id, experiment_id)
    shutil.move(str(path), str(new_path))

    output_file_path = pathlib.Path(
        new_path,
        'dta',
        'output',
        'output_rt_10_sn_2.5.to_excel.txt'
    )

    api.add_dataset(experiment_id, int(user_id), output_file_path)

    set_status('done')


def update_status(user_id, name):
    def status(status):
        redis.hset('user:{}'.format(user_id), name, status)

    return status
