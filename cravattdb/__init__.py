"""Backend for a proteomics database."""
from flask import Flask, render_template, jsonify, request, abort, make_response
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.core import current_user
from flask_mail import Mail
from redis import Redis
from cravattdb.models.search import Search
from cravattdb.models.tasks import process
from cravattdb.models.database import db, User, Role
from http import HTTPStatus
import cravattdb.models.upload as upload
import config.config as config
import cravattdb.models.api as api

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECURITY_REGISTERABLE'] = True
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.EMAIL
app.config['MAIL_PASSWORD'] = config.EMAIL_PASSWORD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis = Redis(host='redis')
mail = Mail(app)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
@login_required
def index():
    meta = current_user.meta
    return render_template('index.html', meta=meta, id=current_user.email)


@app.route('/search/<name>', methods=['POST'])
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


@app.route('/status')
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall(user_id)
    return render_template('index.html', id=current_user.email, info=info)


@app.route('/sideload')
@login_required
def sideload_dataset():
    bootstrap = {
        **api.get_organism(),
        **api.get_probe(),
        **api.get_inhibitor(),
        **api.get_experiment_type()
    }

    return render_template('index.html', bootstrap=bootstrap)


@app.route('/experiments')
@login_required
def get_experiments():
    bootstrap = api.get_experiment(flat=True)
    return render_template('index.html', bootstrap=bootstrap)


@app.route('/dataset/<int:experiment_id>')
@login_required
def get_dataset(experiment_id):
    return render_template('index.html', bootstrap=api.get_dataset(experiment_id))


@app.route('/api/experiment', methods=['PUT'])
@login_required
def add_experiment():
    return jsonify(api.add_experiment(
        name=request.form.get('name'),
        user_id=current_user.get_id(),
        organism_id=request.form.get('organism'),
        experiment_type_id=request.form.get('experimentType'),
        probe_id=request.form.get('probe'),
        inhibitor_id=request.form.get('inhibitor'),
        file=request.files['file']
    ))


@app.route('/api/experiment')
@app.route('/api/experiment/<int:experiment_id>')
def get_experiment(experiment_id=None):
    return jsonify(api.get_experiment(experiment_id))


@app.route('/api/experiment_type')
@app.route('/api/experiment_type/<int:experiment_id>')
def get_experiment_type(experiment_id=None):
    return jsonify(api.get_experiment_type(experiment_id))


@app.route('/api/organism')
@app.route('/api/organism/<int:organism_id>')
def get_organism(organism_id=None):
    return jsonify(api.get_organism(organism_id))


@app.route('/api/probe')
@app.route('/api/probe/<int:probe_id>')
def get_probe(probe_id=None):
    return jsonify(api.get_probe(probe_id))


@app.route('/api/inhibitor')
@app.route('/api/inhibitor/<int:inhibitor_id>')
def get_inhibitor(inhibitor_id=None):
    return jsonify(api.get_inhibitor(inhibitor_id))


@app.route('/api/organism', methods=['PUT'])
def add_organism():
    return jsonify(api.add_organism(
        tax_id=request.args.get('taxId'),
        name=request.args.get('name'),
        display_name=request.args.get('displayName')
    ))


@app.before_first_request
def create_user():
    db.create_all()
    db.session.commit()


def error_response(details, code):
    return make_response(jsonify({'error': details}), code)


@app.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized(error):
    return error_response(error.description, error.code)


@app.errorhandler(HTTPStatus.CONFLICT)
def dataset_exists(error):
    return error_response(error.description, error.code)
