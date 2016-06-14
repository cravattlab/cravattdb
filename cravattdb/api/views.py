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
    return jsonify({'data': model.search(term)})


@api.route('/user_defined')
def get_user_defined():
    return jsonify(model.get_user_defined())


@api.route('/dataset/<int:experiment_id>')
def get_dataset(experiment_id):
    raw = model.get_dataset(experiment_id)

    return jsonify({
        'data': [list(item.values()) for item in raw['dataset']],
        'headers': list(raw['dataset'][0].keys())
    })


@api.route('/experiment')
@api.route('/experiment/<int:experiment_id>')
@login_required
def get_experiment(experiment_id=None):
    return jsonify(model.get_experiment(experiment_id))


@api.route('/experiments')
def get_experiments():
    return jsonify(model.get_experiment(flat=True))


@api.route('/experiment_type')
@api.route('/experiment_type/<int:type_id>')
def get_experiment_type(type_id=None):
    return jsonify(model.get_experiment_type(type_id))


@api.route('/experiment_type', methods=['PUT'])
def add_experiment_type():
    return jsonify(model.add_experiment_type(
        name=request.args.get('name'),
        search_params=request.args.get('searchParams'),
        cimage_params=request.args.get('cimageParams')
    ))


@api.route('/organism')
@api.route('/organism/<int:organism_id>')
def get_organism(organism_id=None):
    return jsonify(model.get_organism(organism_id))


@api.route('/organism', methods=['PUT'])
def add_organism():
    return jsonify(model.add_organism(
        tax_id=request.args.get('taxId'),
        name=request.args.get('name'),
        display_name=request.args.get('displayName')
    ))


@api.route('/instrument')
@api.route('/instrument/<int:instrument_id>')
def get_instrument(instrument_id):
    return jsonify(model.get_instrument(instrument_id))


@api.route('/instrument', methods=['PUT'])
def add_instrument():
    return jsonify(model.add_instrument(
        name=request.args.get('name')
    ))


@api.route('/sample_type')
@api.route('/sample_type/<int:sample_type_id>')
def get_sample_type(sample_type_id):
    return jsonify(model.get_sample_type(sample_type_id))


@api.route('/sample_type', methods=['PUT'])
def add_sample_type():
    return jsonify(model.add_sample_type(
        name=request.args.get('name'),
        description=request.args.get('description')
    ))


@api.route('/cell_type')
@api.route('/cell_type/<int:cell_type_id>')
def get_cell_type(cell_type_id):
    return jsonify(model.get_cell_type(cell_type_id))


@api.route('/cell_type', methods=['PUT'])
def add_cell_type():
    return jsonify(model.add_cell_type(
        name=request.args.get('name'),
        description=request.args.get('description')
    ))


@api.route('/treatment_type')
@api.route('/treatment_type/<int:treatment_type_id>')
def get_treatment_type(treatment_type_id):
    return jsonify(model.get_treatment_type(treatment_type_id))


@api.route('/treatment_type', methods=['PUT'])
def add_treatment_type():
    return jsonify(model.add_treatment_type(
        name=request.args.get('name'),
        description=request.args.get('description')
    ))


@api.route('/proteomic_fraction')
@api.route('/proteomic_fraction/<int:proteomic_fraction_id>')
def get_proteomic_fraction(proteomic_fraction_id):
    return jsonify(model.get_proteomic_fraction(proteomic_fraction_id))


@api.route('/proteomic_fraction', methods=['PUT'])
def add_proteomic_fraction():
    return jsonify(model.add_proteomic_fraction(
        name=request.args.get('name'),
        description=request.args.get('description')
    ))


@api.route('/probe')
@api.route('/probe/<int:probe_id>')
def get_probe(probe_id=None):
    return jsonify(model.get_probe(probe_id))


@api.route('/probe', methods=['PUT'])
def add_probe():
    return jsonify(model.add_probe(
        name=request.args.get('name'),
        iupac_name=request.args.get('iupacName'),
        inchi=request.args.get('inchi')
    ))


@api.route('/inhibitor')
@api.route('/inhibitor/<int:inhibitor_id>')
def get_inhibitor(inhibitor_id=None):
    return jsonify(model.get_inhibitor(inhibitor_id))


@api.route('/inhibitor', methods=['PUT'])
def add_inhibitor():
    return jsonify(model.add_inhibitor(
        name=request.args.get('name'),
        iupac_name=request.args.get('iupacName'),
        inchi=request.args.get('inchi')
    ))


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
