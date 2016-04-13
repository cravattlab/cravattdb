"""Contains definitions of SQLAlchemy tables."""
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    """Simple role or database user."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """User of proteomics database."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    meta = db.Column(JSON)
    experiments = db.relationship(
        'Experiment',
        backref='user',
        lazy='dynamic'
    )
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


class Experiment(db.Model):
    """Holds experimental metadata."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    organism_id = db.Column(db.Integer, db.ForeignKey('organism.id'))
    experiment_type_id = db.Column(db.Integer, db.ForeignKey('experiment_type.id'))
    additional_search_params = db.Column(JSON)
    additional_quant_params = db.Column(JSON)
    annotations = db.Column(JSON)


class Dataset(db.Model):
    """Holds actual experimental dataset."""

    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    peptide_index = db.Column(db.Integer)
    ipi = db.Column(db.String(20))
    description = db.Column(db.Text)
    symbol = db.Column(db.String(20))
    sequence = db.Column(db.String(100))
    mass = db.Column(db.Numeric)
    charge = db.Column(db.Integer)
    segment = db.Column(db.Integer)
    ratio = db.Column(db.Numeric)
    intensity = db.Column(db.Numeric)
    num_ms2_peaks = db.Column(db.Integer)
    num_candidate_peaks = db.Column(db.Integer)
    max_light_intensity = db.Column(db.Numeric)
    light_noise = db.Column(db.Numeric)
    max_heavy_intensity = db.Column(db.Numeric)
    heavy_noise = db.Column(db.Numeric)
    rsquared = db.Column(db.Numeric)
    entry = db.Column(db.Integer)
    link = db.Column(db.String(100))
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class ExperimentType(db.Model):
    """Defines different experiment types."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    search_params = db.Column(JSON)
    cimage_params = db.Column(JSON)
    experiments = db.relationship(
        'Experiment',
        backref='experiment_type',
        lazy='dynamic'
    )


class Organism(db.Model):
    """Holds data related to model organisms."""

    id = db.Column(db.Integer, primary_key=True)
    tax_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    display_name = db.column(db.String(80))
    experiments = db.relationship(
        'Experiment',
        backref='organism',
        lazy='dynamic'
    )
