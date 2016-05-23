"""Blueprint for API methods."""

from flask import Blueprint, request, abort, render_template
from flask.ext.security import login_required
from flask_security.core import current_user
from .search import Search
from .tasks import process
from http import HTTPStatus
from redis import Redis
import cravattdb.auto.upload as upload


auto = Blueprint('auto', __name__,
                 template_folder='templates',
                 static_folder='static')

redis = Redis(host='redis')


@auto.route('/')
@login_required
def render_auto_home():
    return render_template('index.html')


@auto.route('/search/<name>', methods=['POST'])
@login_required
def search(name):
    search = Search(name)

    login = search.login(
        request.form.get('username'),
        request.form.get('password')
    )

    if not login:
        abort(HTTPStatus.UNAUTHORIZED)

    # save RAW files to disk
    # path is type pathlib.Path
    try:
        name, path = upload.upload(
            request.files.getlist('file'),
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
        request.form.get('organism'),
        request.form.get('experiment_type')
    )

    return 'hello'


@auto.route('/status')
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall(user_id)
    return render_template('index.html', id=current_user.email, info=info)
