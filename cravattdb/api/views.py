"""Blueprint for API methods."""

from flask import Blueprint, jsonify, request
from flask.ext.security import login_required
from flask_security.core import current_user
from cravattdb.home.sideload import sideload_experiment
import cravattdb.api.api as model

api = Blueprint('api', __name__,
                template_folder='templates',
                static_folder='static')


@api.route('/search/<string:term>')
def search(term):
    return term


@api.route('/dataset/<int:experiment_id>')
def get_dataset(experiment_id):
    raw = model.get_dataset(experiment_id)

    return jsonify({
        'data': [list(item.values()) for item in raw['dataset']]
    })


@api.route('/experiments')
def get_experiments():
    return jsonify(model.get_experiment(flat=True))


@api.route('/sideload', methods=['PUT'])
@login_required
def sideload():
    return jsonify(sideload_experiment(
        name=request.form.get('name'),
        user_id=current_user.get_id(),
        organism_id=request.form.get('organism'),
        experiment_type_id=request.form.get('type'),
        probe_id=request.form.get('probe'),
        inhibitor_id=request.form.get('inhibitor'),
        file=request.files['file']
    ))


@api.route('/experiment')
@api.route('/experiment/<int:experiment_id>')
@login_required
def get_experiment(experiment_id=None):
    return jsonify(model.get_experiment(experiment_id))


@api.route('/experiment_type')
@api.route('/experiment_type/<int:experiment_id>')
def get_experiment_type(experiment_id=None):
    return jsonify(model.get_experiment_type(experiment_id))


@api.route('/organism')
@api.route('/organism/<int:organism_id>')
def get_organism(organism_id=None):
    return jsonify(model.get_organism(organism_id))


@api.route('/probe')
@api.route('/probe/<int:probe_id>')
def get_probe(probe_id=None):
    return jsonify(model.get_probe(probe_id))


@api.route('/inhibitor')
@api.route('/inhibitor/<int:inhibitor_id>')
def get_inhibitor(inhibitor_id=None):
    return jsonify(model.get_inhibitor(inhibitor_id))


@api.route('/organism', methods=['PUT'])
def add_organism():
    return jsonify(model.add_organism(
        tax_id=request.args.get('taxId'),
        name=request.args.get('name'),
        display_name=request.args.get('displayName')
    ))


@api.route('/experimentType', methods=['PUT'])
def add_experiment_type():
    return jsonify(model.add_experiment_type(
        name=request.args.get('name'),
        search_params=request.args.get('searchParams'),
        cimage_params=request.args.get('cimageParams')
    ))


@api.route('/probe', methods=['PUT'])
def add_probe():
    return jsonify(model.add_probe(
        name=request.args.get('name'),
        iupac_name=request.args.get('iupacName'),
        inchi=request.args.get('inchi')
    ))


@api.route('/inhibitor', methods=['PUT'])
def add_inhibitor():
    return jsonify(model.add_inhibitor(
        name=request.args.get('name'),
        iupac_name=request.args.get('iupacName'),
        inchi=request.args.get('inchi')
    ))
