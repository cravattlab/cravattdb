from celery import Celery
from pathlib import PurePath
import models.convert as convert
import models.quantify as quantify

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def process(search, name, path, organism, experiment_type):
    # convert .raw to .ms2
    # removing first bit of file path since that is the upload folder
    convert_status = convert.convert(PurePath(*path.parts[1:]).as_posix())

    converted_paths = [ path.joinpath(f) for f in convert_status['files_converted'] ]

    # initiate IP2 search
    dta_select_link = search.search(
        organism,
        experiment_type,
        [ f for f in converted_paths if f.suffix == '.ms2']
    )

    # quantify all of the things
    return quantify.quantify(
        name,
        dta_select_link,
        experiment_type,
        path
    )