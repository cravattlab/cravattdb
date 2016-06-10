"""Defines methods for interacting with database."""
from cravattdb import db
from collections import OrderedDict as OrderedDict
from cravattdb.home.models import (
    Experiment, Dataset, ExperimentType, Organism, Probe, Inhibitor,
    OrganismSchema, ExperimentTypeSchema, ExperimentSchema, DatasetSchema, ProbeSchema, InhibitorSchema
)
import csv
import itertools
import statistics


experiment_schema = ExperimentSchema()
dataset_schema = DatasetSchema(many=True)
dataset_schema_summary = DatasetSchema(many=True, only=(
    'uniprot', 'symbol', 'description', 'sequence',
    'mass', 'charge', 'segment', 'ratio', 'entry'
))
dataset_schema_search = DatasetSchema(many=True, only=(
    'id', 'uniprot', 'symbol', 'description', 'sequence', 'ratio',
    'experiment_id'
))
organism_schema = OrganismSchema()
experiment_type_schema = ExperimentTypeSchema()
probe_schema = ProbeSchema()
inhibitor_schema = InhibitorSchema()


def search(term):
    data = Dataset.query.filter(
        (Dataset.uniprot.ilike(term)) |
        (Dataset.symbol.ilike('{}%'.format(term))) |
        (Dataset.description.ilike('%{}%'.format(term)))
    )

    result = dataset_schema_search.dump(data).data['dataset']

    sorted_result = sorted(result, key=lambda x: x.get('uniprot'))
    grouped_result = itertools.groupby(sorted_result, key=lambda x: x.get('uniprot'))

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
                'experiment': get_experiment(items[0]['experiment_id']),
                'mean_ratio': '{:.2f}'.format(statistics.mean(ratios)),
                'qp': len(ratios)
            })

        groups.append(temp)

    return groups


def add_experiment(name, user_id, organism_id, experiment_type_id, probe_id=0, inhibitor_id=0):
    experiment = experiment_schema.load({
        'name': name,
        'user_id': int(user_id),
        'organism_id': int(organism_id),
        'experiment_type_id': int(experiment_type_id),
        'probe_id': int(probe_id or 0) or None,
        'inhibitor_id': int(inhibitor_id or 0) or None
    })

    db.session.add(experiment.data)
    db.session.commit()

    result = experiment_schema.dump(experiment.data)
    return result.data


def add_experiment_with_data(name, user_id, organism_id, experiment_type_id, file, probe_id=0, inhibitor_id=0):
    experiment = add_experiment(
        name=name,
        user_id=user_id,
        organism_id=organism_id,
        experiment_type_id=experiment_type_id,
        probe_id=probe_id,
        inhibitor_id=inhibitor_id
    )

    add_dataset(experiment['id'], user_id, file)

    return experiment


def add_dataset(experiment_id, user_id, output_file_path):
    delchars = {ord(c): None for c in map(chr, range(256)) if not c.isalpha()}

    with output_file_path.open('r') as f:
        # skip first line
        f.readline()

        for line in csv.reader(f, delimiter='\t'):
            db.session.add(Dataset(
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


def get_experiment(experiment_id=None, flat=False):
    many = experiment_id is None

    if many:
        experiment = Experiment.query.all()
    else:
        experiment = Experiment.query.get(experiment_id)

    result = experiment_schema.dump(experiment, many=many)

    if flat:
        if many:
            raw = result.data['experiments']
        else:
            raw = [result.data]

        desired_keys = [
            'id',
            'name',
            'organism',
            'probe',
            'inhibitor',
            'date'
        ]

        filtered = []

        for experiment in raw:
            ordered = OrderedDict()

            for key in desired_keys:
                ordered[key] = experiment[key]

            filtered.append(ordered)

        for item in filtered:
            item['organism'] = item['organism']['name']

            if item['inhibitor']:
                item['inhibitor'] = item['inhibitor']['name']

            if item['probe']:
                item['probe'] = item['probe']['name']

        return {
            'headers': list(filtered[0].keys()),
            'data': [list(item.values()) for item in filtered]
        }
    else:
        return result.data


def get_dataset(experiment_id):
    dataset = Dataset.query.filter_by(experiment_id=experiment_id)
    result = dataset_schema_summary.dump(dataset).data

    return result


def get_experiment_type(experiment_id=None):
    if experiment_id:
        experiment_type = ExperimentType.query.get(experiment_id)
    else:
        experiment_type = ExperimentType.query.all()

    result = experiment_type_schema.dump(experiment_type, many=experiment_id is None)
    return result.data


def get_organism(organism_id=None):
    if organism_id:
        organism = Organism.query.get(organism_id)
    else:
        organism = Organism.query.all()

    result = organism_schema.dump(organism, many=organism_id is None)
    return result.data


def get_probe(probe_id=None):
    if probe_id:
        probe = Probe.query.get(probe_id)
    else:
        probe = Probe.query.all()

    result = probe_schema.dump(probe, many=probe_id is None)
    return result.data


def get_inhibitor(inhibitor_id=None):
    if inhibitor_id:
        inhibitor = Inhibitor.query.get(inhibitor_id)
    else:
        inhibitor = Inhibitor.query.all()

    result = inhibitor_schema.dump(inhibitor, many=inhibitor_id is None)
    return result.data


def add_organism(tax_id, name, display_name):
    organism = organism_schema.load({
        'tax_id': tax_id,
        'name': name,
        'display_name': display_name
    })

    db.session.add(organism.data)
    db.session.commit()
    result = organism_schema.dump(organism.data)

    return result.data


def delete_organism(organism_id):
    organism = Organism.query.get(organism_id)

    if organism:
        db.session.delete(organism)
        db.session.commit()
        return True
    else:
        return False


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
