from models.database import db
from sqlalchemy.dialects.postgresql import JSON

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    path = db.Column(db.String(80))
    date = db.Column(db.DateTime())
    user = db.relationship('User')
    organism = db.relationship('Organism')
    experiment_type = db.relationship('ExperimentType')
    additional_search_params = db.Column(JSON)
    additional_quant_params = db.Column(JSON)
    annotations = db.Column(JSON)

    def __init__(self, name, path, date, user, organism, experiment_type, additional_search_params, additional_quant_params, annotations):
        self.name = name
        self.path = path
        self.date = date
        self.user = user
        self.organism = organism
        self.experiment_type = experiment_type
        self.additional_search_params = additional_search_params
        self.additional_quant_params = additional_quant_params
        self.annotations = annotations

class ExperimentType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    search_params = db.Column(JSON)
    cimage_params = db.Column(JSON)

    def __init__(self, name, search_params, cimage_params):
        self.name = name
        self.search_params = search_params
        self.cimage_params = cimage_params

class Organism(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tax_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    display_name = db.column(db.String(80))

    def __init__(self, tax_id, name, display_name):
        self.tax_id = tax_id
        self.name = name
        self.display_name = display_name