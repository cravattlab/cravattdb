"""Define processing actions for celery task queue."""
from celery import Celery
from pathlib import PurePath
from redis import StrictRedis
import cravattdb.auto.convert as convert
import cravattdb.auto.quantify as quantify
import config.config as config

app = Celery('tasks', broker='amqp://guest@rabbitmq//')

redis = StrictRedis(host='redis')


@app.task
def process(search, user_id, name, path, organism, experiment_type):
    # convert .raw to .ms2
    # removing first bit of file path since that is the upload folder
    set_status = update_status(user_id, name)
    set_status('converting')

    convert_status = convert.convert(PurePath(path).relative_to(config.UPLOAD_FOLDER).as_posix())
    converted_paths = [path.joinpath(f) for f in convert_status['files_converted']]
    set_status('searching ip2')

    # initiate IP2 search
    dta_select_link = search.search(
        organism,
        experiment_type,
        [f for f in converted_paths if f.suffix == '.ms2']
    )

    set_status('quantification')

    # quantify all of the things
    final = quantify.quantify(
        name,
        dta_select_link,
        experiment_type,
        path
    )

    set_status('all done')
    return final


def update_status(user_id, name):
    def status(status):
        redis.hset('user:{}'.format(user_id), name, status)

    return status
