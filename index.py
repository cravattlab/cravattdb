"""Backend for a proteomics database."""
from flask import Flask, render_template, jsonify, request, abort, make_response
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.core import current_user
from flask_mail import Mail
from redis import Redis
from models.search import Search
from models.tasks import process
from models.database import db, User, Role, Experiment, ExperimentType, Organism, OrganismSchema, ExperimentTypeSchema
from http import HTTPStatus
import models.upload as upload
import config.config as config
import models.sideload as sideload

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

redis = Redis(host='redis')
mail = Mail(app)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

organism_schema = OrganismSchema()
organisms_schema = OrganismSchema(many=True)
experiment_type_schema = ExperimentTypeSchema()
experiment_types_schema = ExperimentTypeSchema(many=True)


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


@app.route('/status', methods=['GET'])
@login_required
def status():
    user_id = current_user.get_id()
    info = redis.hgetall(user_id)
    return render_template('index.html', id=current_user.email, info=info)


@app.route('/sideload', methods=['GET', 'POST'])
@login_required
def sideload_dataset():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        experiment = Experiment(
            name=request.form.get('name'),
            user_id=current_user.get_id(),
            organism_id=request.form.get('organism'),
            experiment_type_id=request.form.get('experiment_type')
        )

        db.session.add(experiment)

        sideload.new_dataset(
            request.form.get('experiment_type'),
            request.form.get('experiment_id'),
            request.files['file']
        )

        db.session.commit()

        return 'hello'


@app.route('/api/experiment_type', methods=['GET', 'POST'])
@app.route('/api/experiment_type/<int:experiment_id>', methods=['GET', 'POST'])
def get_experiment_type(experiment_id=None):
    if experiment_id:
        experiment_type = ExperimentType.query.get(experiment_id)
        result = experiment_type_schema.dump(experiment_type)
    else:
        experiment_types = ExperimentType.query.all()
        result = experiment_types_schema.dump(experiment_types)

    return jsonify(result.data)


@app.route('/api/organism', methods=['GET', 'POST'])
@app.route('/api/organism/<int:organism_id>', methods=['GET', 'POST'])
def get_organism(organism_id=None):
    if organism_id:
        organism = Organism.query.get(organism_id)
        result = organism_schema.dump(organism)
    else:
        organisms = Organism.query.all()
        result = organisms_schema.dump(organisms)

    return jsonify(result.data)


@app.route('/api/organism', methods=['PUT'])
def add_organism():
    organism = organism_schema.load({
        'tax_id': request.args.get('taxId'),
        'name': request.args.get('name'),
        'display_name': request.args.get('displayName')
    })

    db.session.add(organism.data)
    db.session.commit()
    result = organism_schema.dump(organism.data)

    return jsonify(result.data)


@app.route('/api/organism/<int:organism_id>', methods=['DELETE'])
def delete_organism(organism_id):
    organism = Organism.query.get(organism_id)

    if organism:
        db.session.delete(organism)
        db.session.commit()
    else:
        return ('', HTTPStatus.NOT_FOUND)

    return ('', HTTPStatus.NO_CONTENT)


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
