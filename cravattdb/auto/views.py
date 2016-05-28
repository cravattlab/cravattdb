"""Blueprint for API methods."""

from flask import Blueprint, request, abort, render_template
from flask.ext.security import login_required
from flask_security.core import current_user
from .search import Search
from .tasks import process
from cravattdb.home.models import ExperimentType, Organism
from http import HTTPStatus
from redis import StrictRedis
import cravattdb.auto.upload as upload


auto = Blueprint('auto', __name__,
                 template_folder='templates',
                 static_folder='static')

redis = StrictRedis(host='redis')


@auto.route('/')
@login_required
def render_auto_home():
    return render_template('index.html')


@auto.route('/search', methods=['POST'])
@login_required
def search():
    name = request.form.get('name')
    search = Search(name)

    login = search.login(
        request.form.get('ip2_username'),
        request.form.get('ip2_password')
    )

    if not login:
        abort(HTTPStatus.UNAUTHORIZED)

    # save RAW files to disk
    # path is type pathlib.Path
    try:
        name, path = upload.upload(
            request.files.getlist('files'),
            current_user.get_id(),
            name
        )
    except FileExistsError:
        abort(HTTPStatus.CONFLICT)

    organism_id = request.form.get('organism')
    experiment_type_id = request.form.get('type')

    # continue processing in background with celery
    process.delay(
        search=search,
        user_id=current_user.get_id(),
        name=name,
        path=path,
        organism_id=organism_id,
        organism_name=Organism.query.get(organism_id).display_name,
        experiment_type_id=experiment_type_id,
        experiment_type_name=ExperimentType.query.get(experiment_type_id).name,
        probe_id=int(request.form.get('probe')),
        inhibitor_id=int(request.form.get('inhibitor'))
    )

    return 'hello'


@auto.route('/status')
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall('user:{}'.format(user_id))
    return render_template('index.html', id=current_user.email, info=info)
