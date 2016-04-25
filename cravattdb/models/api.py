"""Defines methods for interacting with database."""
from cravattdb.models.database import (
    db,
    Experiment, ExperimentType, Organism, Probe, Inhibitor,
    OrganismSchema, ExperimentTypeSchema, ExperimentSchema, ProbeSchema, InhibitorSchema

)


experiment_schema = ExperimentSchema()
experiments_schema = ExperimentSchema(many=True)
organism_schema = OrganismSchema()
organisms_schema = OrganismSchema(many=True)
experiment_type_schema = ExperimentTypeSchema()
experiment_types_schema = ExperimentTypeSchema(many=True)
probe_schema = ProbeSchema()
probes_schema = ProbeSchema(many=True)
inhibitor_schema = InhibitorSchema()
inhibitors_schema = InhibitorSchema(many=True)


def add_experiment(name, user_id, organism_id, experiment_type_id, probe_id=0, inhibitor_id=0):
    experiment = experiment_schema.load({
        'name': name,
        'user_id': int(user_id),
        'organism_id': int(organism_id),
        'experiment_type_id': int(experiment_type_id),
        'probe_id': int(probe_id),
        'inhibitor_id': int(inhibitor_id)
    })

    print(experiment)

    db.session.add(experiment.data)
    db.session.commit()
    result = organism_schema.dump(experiment.data)

    return result.data


def get_experiment(experiment_id=None):
    if experiment_id:
        experiment = Experiment.query.get(experiment_id)
        result = experiment_schema.dump(experiment)
    else:
        experiments = Experiment.query.all()
        result = experiments_schema.dump(experiments)

    return result.data


def get_experiment_type(experiment_id=None):
    if experiment_id:
        experiment_type = ExperimentType.query.get(experiment_id)
        result = experiment_type_schema.dump(experiment_type)
    else:
        experiment_types = ExperimentType.query.all()
        result = experiment_types_schema.dump(experiment_types)

    return result.data


def get_organism(organism_id=None):
    if organism_id:
        organism = Organism.query.get(organism_id)
        result = organism_schema.dump(organism)
    else:
        organisms = Organism.query.all()
        result = organisms_schema.dump(organisms)

    return result.data


def get_probe(probe_id=None):
    if probe_id:
        probe = Probe.query.get(probe_id)
        result = probe_schema.dump(probe)
    else:
        probes = Probe.query.all()
        result = probes_schema.dump(probes)

    return result.data


def get_inhibitor(inhibitor_id=None):
    if inhibitor_id:
        inhibitor = Inhibitor.query.get(inhibitor_id)
        result = inhibitor_schema.dump(inhibitor)
    else:
        inhibitors = Inhibitor.query.all()
        result = inhibitors_schema.dump(inhibitors)

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
