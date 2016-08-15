"""Defines methods for interacting with database."""
from cravattdb import db
from sqlalchemy import func
from cravattdb.utils.fun import special_median
from cravattdb.users.models import User, UserSchema
import cravattdb.shared.constants as constants
import cravattdb.contrib.residue_number_annotation as residue_number_annotation
import cravattdb.home.models as m
import csv
import itertools

experiment_schema = m.ExperimentSchema()
treatment_schema = m.TreatmentSchema()
dataset_schema = m.DatasetSchema(many=True, exclude='experiment')
dataset_schema_summary = m.DatasetSchema(only=(
    'uniprot', 'symbol', 'description', 'sequence',
    'mass', 'charge', 'segment', 'ratio', 'entry',
    'rsquared'
), exclude='experiment', many=True)
dataset_schema_search = m.DatasetSchema(only=(
    'experiment_id', 'experiment', 'uniprot', 'symbol', 'description', 'ratio', 'rsquared'
), many=True)
organism_schema = m.OrganismSchema()
experiment_type_schema = m.ExperimentTypeSchema()
instrument_schema = m.InstrumentSchema()
sample_type_schema = m.SampleTypeSchema()
cell_type_schema = m.CellTypeSchema()
proteomic_fraction_schema = m.ProteomicFractionSchema()
probe_schema = m.ProbeSchema()
inhibitor_schema = m.InhibitorSchema()
user_schema = UserSchema()


def _get_all(model, schema):
    query = model.query.all()
    return schema.dump(query, many=True).data


def _get_all_or_one(model, schema, _id=None):
    """Helper method which returns all results if _id is undefined.

    Arguments:
        model -- SQLAlchemy Model to query against
        schema -- Marhsmallow schema to use when dumping data
        _id  -- Optional primary key to query against.
    """
    if _id:
        query = model.query.get(_id)
    else:
        query = model.query.all()

    return schema.dump(query, many=_id is None).data


def get_user_defined():
    """Return all user definable types.

    Utility method for use with forms and filters. Collects all user defined
    *things* and returns them in one object. Saves on requests.
    """
    return {
        **_get_all(m.ExperimentType, experiment_type_schema),
        **_get_all(m.Organism, organism_schema),
        **_get_all(m.Probe, probe_schema),
        **_get_all(m.Inhibitor, inhibitor_schema),
        **_get_all(m.SampleType, sample_type_schema),
        **_get_all(m.Instrument, instrument_schema),
        **_get_all(m.CellType, cell_type_schema),
        **_get_all(m.ProteomicFraction, proteomic_fraction_schema),
        **_get_all(User, user_schema)
    }


def get_available_filters():
    """Return list of all filters."""
    user_defined = get_user_defined()
    result = []

    for item, data in user_defined.items():
        # depluralize using the most naive method possible
        if item.endswith('s'):
            item = item[:-1]

        result.append({
            'name': item,
            'display': item.replace('_', ' ').title(),
            'options': data
        })

    return {'data': result}


def search(params):
    term = params.pop('term')

    query = db.session.query(
        m.Dataset
    ).join(m.Experiment).filter(
        (func.lower(m.Dataset.symbol).like('{}%'.format(term.lower()))) |
        (m.Dataset.uniprot == term.upper()) |
        (m.Dataset.description.ilike('%{}%'.format(term)))
    )

    query = filter_query(query, params).order_by(m.Dataset.uniprot)
    result = dataset_schema_search.dump(query).data['dataset']

    grouped_result = itertools.groupby(result, key=lambda x: x.get('uniprot'))
    groups = []

    for uniprot, group in grouped_result:
        x = list(group)

        temp = {
            'uniprot': uniprot,
            'description': x[0]['description'],
            'symbol': x[0]['symbol'],
            'data': []
        }

        experiment_sorted = sorted(list(x), key=lambda x: x.get('experiment_id'))
        by_experiment = itertools.groupby(experiment_sorted, key=lambda x: x.get('experiment_id'))

        for experiment_id, g in by_experiment:
            items = list(g)
            experiment = items[0]['experiment']
            experiment.update(_aggregate_treatment_data(experiment.pop('treatments')))
            # filter ratios through rsquared cutoff
            ratios = [x['ratio'] for x in items if x['rsquared'] > constants.RSQUARED_CUTOFF]

            temp['data'].append({
                'experiment': experiment,
                'median_ratio': '{:.2f}'.format(special_median(ratios)),
                'qp': len(ratios)
            })

        groups.append(temp)

    return groups


def filter_query(query, filters):
    """Apply filters to a query."""
    for key, value in filters.items():
        column = getattr(m.Experiment, key, None)

        if not column:
            continue

        if ',' in value:
            query = query.filter(column.in_(value.split(',')))
        else:
            query = query.filter(column == value)

    return query


def _aggregate_treatment_data(data):
    types = ['inhibitor', 'probe']
    aggregate = dict.fromkeys(types)

    for t in types:
        names = [y[t]['name'] for y in [x for x in data if x[t]]]
        aggregate[t] = ', '.join(list(set(names)))

    return aggregate


def get_dataset(experiment_id):
    dataset = m.Dataset.query.filter_by(experiment_id=experiment_id)
    return dataset_schema_summary.dump(dataset).data


def add_dataset(experiment_id, user_id, output_file_path):
    delchars = {ord(c): None for c in map(chr, range(256)) if not c.isalpha()}

    experiment_type = get_experiment(experiment_id)['experiment_type']['name']
    get_residue_number = residue_number_annotation.get_residue_number(experiment_type)

    with output_file_path.open('r') as f:
        # skip first line
        f.readline()

        for line in csv.reader(f, delimiter='\t'):
            db.session.add(m.Dataset(
                peptide_index=line[0],
                uniprot=line[1],
                description=line[2],
                symbol=line[3],
                sequence=line[4],
                clean_sequence=line[4].translate(delchars),
                residue_number=get_residue_number(line[1], line[4]) if get_residue_number else None,
                mass=line[5],
                charge=line[6],
                segment=line[7],
                ratio=line[8],
                intensity=line[9],
                num_ms2_peaks=line[10].split('/')[0],
                num_candidate_peaks=line[10].split('/')[1],
                max_light_intensity=line[10].split('/')[2],
                light_noise=line[10].split('/')[3],
                max_heavy_intensity=line[10].split('/')[4],
                heavy_noise=line[10].split('/')[5],
                rsquared=line[11],
                entry=line[12],
                experiment_id=experiment_id
            ))

    db.session.commit()


def get_protein_from_dataset(experiment_id, uniprot_id):
    dataset = m.Dataset.query.filter_by(
        experiment_id=experiment_id,
        uniprot=uniprot_id
    )
    return dataset_schema_summary.dump(dataset).data


def get_peptide_from_dataset(experiment_id, sequence):
    dataset = m.Dataset.query.filter_by(
        experiment_id=experiment_id,
        clean_sequence=sequence
    )
    return dataset_schema_summary.dump(dataset).data


def get_experiment(experiment_id=None, flat=False):
    data = _get_all_or_one(m.Experiment, experiment_schema, experiment_id)

    if 'experiments' in data:
        experiments = data['experiments']
    else:
        experiments = [data]

    for ex in experiments:
        ex.update(_aggregate_treatment_data(ex['treatments']))

    return data


def add_experiment(data):
    experiment = experiment_schema.load(data)
    db.session.add(experiment.data)
    db.session.commit()
    return experiment_schema.dump(experiment.data).data


def get_treatment(experiment_id):
    treatment = m.Treatment.query.filter_by(experiment_id=experiment_id)
    return treatment_schema.dump(treatment).data


def add_treatment(data):
    treatment = treatment_schema.load(data)
    print(treatment)
    db.session.add(treatment.data)
    db.session.commit()
    return treatment_schema.dump(treatment.data).data


def get_experiment_type(experiment_id=None):
    return _get_all_or_one(m.ExperimentType, experiment_type_schema, experiment_id)


def add_experiment_type(name, search_params, cimage_params):
    experiment_type = experiment_type_schema.load({
        'name': name,
        'search_params': search_params,
        'cimage_params': cimage_params
    })

    db.session.add(experiment_type.data)
    db.session.commit()
    result = experiment_type_schema.dump(experiment_type.data)

    return result.data


def get_organism(organism_id=None):
    return _get_all_or_one(m.Organism, organism_schema, organism_id)


def add_organism(tax_id, name, scientific_name):
    organism = organism_schema.load({
        'tax_id': tax_id,
        'name': name,
        'scientific_name': scientific_name
    })

    db.session.add(organism.data)
    db.session.commit()
    result = organism_schema.dump(organism.data)

    return result.data


def get_instrument(instrument_id=None):
    return _get_all_or_one(m.Instrument, instrument_schema, instrument_id)


def add_instrument(name):
    instrument = instrument_schema.load({
        'name': name
    })

    db.session.add(instrument.data)
    db.session.commit()
    result = instrument_schema.dump(instrument.data)
    return result.data


def get_sample_type(sample_type_id=None):
    return _get_all_or_one(m.SampleType, sample_type_schema, sample_type_id)


def add_sample_type(name, description):
    sample_type = sample_type_schema.load({
        'name': name,
        'description': description
    })

    db.session.add(sample_type.data)
    db.session.commit()
    result = sample_type_schema.dump(sample_type.data)
    return result.data


def get_cell_type(cell_type_id=None):
    return _get_all_or_one(m.CellType, cell_type_schema, cell_type_id)


def add_cell_type(name, description):
    cell_type = cell_type_schema.load({
        'name': name,
        'description': description
    })

    db.session.add(cell_type.data)
    db.session.commit()
    result = cell_type_schema.dump(cell_type.data)
    return result.data


def get_proteomic_fraction(proteomic_fraction_id=None):
    return _get_all_or_one(m.ProteomicFraction, proteomic_fraction_schema, proteomic_fraction_id)


def add_proteomic_fraction(name, description):
    proteomic_fraction = proteomic_fraction_schema.load({
        'name': name,
        'description': description
    })

    db.session.add(proteomic_fraction.data)
    db.session.commit()
    result = proteomic_fraction_schema.dump(proteomic_fraction.data)
    return result.data


def get_probe(probe_id=None):
    return _get_all_or_one(m.Probe, probe_schema, probe_id)


def add_probe(name, iupac_name, inchi):
    probe = probe_schema.load({
        'name': name,
        'iupac_name': iupac_name,
        'inchi': inchi
    })

    db.session.add(probe.data)
    db.session.commit()
    result = probe_schema.dump(probe.data)

    return result.data


def get_inhibitor(inhibitor_id=None):
    return _get_all_or_one(m.Inhibitor, inhibitor_schema, inhibitor_id)


def add_inhibitor(name, iupac_name, inchi):
    inhibitor = inhibitor_schema.load({
        'name': name,
        'iupac_name': iupac_name,
        'inchi': inchi
    })

    db.session.add(inhibitor.data)
    db.session.commit()
    result = inhibitor_schema.dump(inhibitor.data)

    return result.data
