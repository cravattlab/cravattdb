"""Defines methods for interacting with database."""
import cravattdb.models.sideload as sideload
from collections import OrderedDict as OrderedDict
from cravattdb.models.database import (
    db,
    Experiment, Dataset, ExperimentType, Organism, Probe, Inhibitor,
    OrganismSchema, ExperimentTypeSchema, ExperimentSchema, DatasetSchema, ProbeSchema, InhibitorSchema
)


experiment_schema = ExperimentSchema()
dataset_schema = DatasetSchema(many=True)
dataset_schema_summary = DatasetSchema(many=True, only=(
    'peptide_index', 'ipi', 'symbol', 'description', 'sequence',
    'mass', 'charge', 'segment', 'ratio'
))
organism_schema = OrganismSchema()
experiment_type_schema = ExperimentTypeSchema()
probe_schema = ProbeSchema()
inhibitor_schema = InhibitorSchema()


def add_experiment(name, user_id, organism_id, experiment_type_id, file, probe_id=0, inhibitor_id=0):
    experiment = experiment_schema.load({
        'name': name,
        'user_id': int(user_id),
        'organism_id': int(organism_id),
        'experiment_type_id': int(experiment_type_id),
        'probe_id': int(probe_id),
        'inhibitor_id': int(inhibitor_id)
    })

    db.session.add(experiment.data)
    db.session.commit()

    # after commit since we need to get id
    sideload.new_dataset(experiment.data.id, file)

    result = organism_schema.dump(experiment.data)

    return result.data


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
            item['inhibitor'] = item['inhibitor']['name']
            item['probe'] = item['probe']['name']

        return {
            'headers': list(filtered[0].keys()),
            'data': [list(item.values()) for item in filtered]
        }
    else:
        return result.data


def get_dataset(experiment_id):
    for i in range(2):
        try:
            dataset = Dataset.query.filter_by(experiment_id=experiment_id)
            result = dataset_schema_summary.dump(dataset).data
            break
        except AssertionError:
            # class definition for dynamic class does not exist on current metadata
            sideload.create_dataset(experiment_id)

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
