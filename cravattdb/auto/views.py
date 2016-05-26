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

    # continue processing in background with celery
    process.delay(
        search,
        current_user.get_id(),
        name,
        path,
        Organism.query.get(request.form.get('organism')).display_name,
        ExperimentType.query.get(request.form.get('type')).name
    )

    return 'hello'


@auto.route('/status')
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall('user:{}'.format(user_id))
    return render_template('index.html', id=current_user.email, info=info)
