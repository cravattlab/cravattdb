"""Defines methods for interacting with database."""
from cravattdb import db
import cravattdb.home.models as m
import csv
import itertools
import statistics

experiment_schema = m.ExperimentSchema()
treatment_schema = m.TreatmentSchema()
dataset_schema = m.DatasetSchema(many=True)
dataset_schema_summary = m.DatasetSchema(many=True, only=(
    'uniprot', 'symbol', 'description', 'sequence',
    'mass', 'charge', 'segment', 'ratio', 'entry'
))
dataset_schema_search = m.DatasetSchema(many=True, only=(
    'id', 'uniprot', 'symbol', 'description', 'sequence', 'ratio',
    'experiment_id'
))
organism_schema = m.OrganismSchema()
experiment_type_schema = m.ExperimentTypeSchema()
instrument_schema = m.InstrumentSchema()
sample_type_schema = m.SampleTypeSchema()
cell_type_schema = m.CellTypeSchema()
proteomic_fraction_schema = m.ProteomicFractionSchema()
probe_schema = m.ProbeSchema()
inhibitor_schema = m.InhibitorSchema()


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
        **_get_all(m.ProteomicFraction, proteomic_fraction_schema)
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


def search(term):
    data = m.Dataset.query.filter(
        (m.Dataset.uniprot.ilike(term)) |
        (m.Dataset.symbol.ilike('{}%'.format(term))) |
        (m.Dataset.description.ilike('%{}%'.format(term)))
    )

    result = dataset_schema_search.dump(data).data['dataset']

    sorted_result = sorted(result, key=lambda x: x.get('uniprot'))
    grouped_result = itertools.groupby(sorted_result, key=lambda x: x.get('uniprot'))

    # grab ids so we can look up experiment info by batch
    experiment_ids = [item.get('experiment_id') for item in result]
    experiments_data = get_experiments(set(experiment_ids))['experiments']
    experiments = {ex['id']: ex for ex in experiments_data}

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

            ratios = [x['ratio'] for x in items]

            temp['data'].append({
                'experiment': experiments[experiment_id],
                'mean_ratio': '{:.2f}'.format(statistics.mean(ratios)),
                'qp': len(ratios)
            })

        groups.append(temp)

    return groups


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


def get_experiments(experiment_ids):
    experiments = m.Experiment.query.filter(m.Experiment.id.in_(experiment_ids))
    data = experiment_schema.dump(experiments, many=True).data

    for ex in data['experiments']:
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
