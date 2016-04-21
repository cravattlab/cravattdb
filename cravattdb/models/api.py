"""Defines methods for interacting with database."""
from models.database import (
    db,
    Experiment, ExperimentType, Organism,
    OrganismSchema, ExperimentTypeSchema, ExperimentSchema
)


experiment_schema = ExperimentSchema()
experiments_schema = ExperimentSchema(many=True)
organism_schema = OrganismSchema()
organisms_schema = OrganismSchema(many=True)
experiment_type_schema = ExperimentTypeSchema()
experiment_types_schema = ExperimentTypeSchema(many=True)


def add_experiment(name, user_id, organism_id, experiment_type):
    experiment = experiment_schema.load({
        'name': name,
        'user_id': user_id,
        'organism_id': organism_id,
        'experiment_type_id': experiment_type
    })

    db.session.add(experiment.data)
    db.session.commit()
    result = organism_schema.dump(experiment.data)

    result.data


def get_experiment(experiment_id):
    if experiment_id:
        experiment = Experiment.query.get(experiment_id)
        result = experiment_schema.dump(experiment)
    else:
        experiments = Experiment.query.all()
        result = experiments_schema.dump(experiments)

    return result


def get_experiment_type(experiment_id):
    if experiment_id:
        experiment_type = ExperimentType.query.get(experiment_id)
        result = experiment_type_schema.dump(experiment_type)
    else:
        experiment_types = ExperimentType.query.all()
        result = experiment_types_schema.dump(experiment_types)

    return result


def get_organism(organism_id):
    if organism_id:
        organism = Organism.query.get(organism_id)
        result = organism_schema.dump(organism)
    else:
        organisms = Organism.query.all()
        result = organisms_schema.dump(organisms)

    return result


def add_organism(tax_id, name, display_name):
    organism = organism_schema.load({
        'tax_id': tax_id,
        'name': name,
        'display_name': display_name
    })

    db.session.add(organism.data)
    db.session.commit()
    result = organism_schema.dump(organism.data)

    return result


def delete_organism(organism_id):
    organism = Organism.query.get(organism_id)

    if organism:
        db.session.delete(organism)
        db.session.commit()
        return True
    else:
        return False
