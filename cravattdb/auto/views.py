"""Blueprint for API methods."""

from flask import Blueprint, request, abort, render_template
from flask_security import login_required, current_user
from .search import Search
from .tasks import process
from cravattdb.home.models import ExperimentType, Organism
from http import HTTPStatus
from redis import StrictRedis
import cravattdb.auto.upload as upload
import json


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
    data = json.loads(request.form.get('data'))
    search = Search(data['name'])

    login = search.login(data['ip2_username'], data['ip2_password'])

    if not login:
        abort(HTTPStatus.UNAUTHORIZED)

    # save RAW files to disk
    # path is type pathlib.Path
    try:
        name, path = upload.upload(
            request.files.getlist('files'),
            current_user.get_id(),
            data['name']
        )
    except FileExistsError:
        abort(HTTPStatus.CONFLICT)

    data.update({'name': name})

    # continue processing in background with celery
    process.delay(data, search, current_user.get_id(), path)
    return 'processing'


@auto.route('/status')
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall('user:{}'.format(user_id))
    return render_template('index.html', id=current_user.email, info=info)
