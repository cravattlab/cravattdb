"""Contains definitions of SQLAlchemy tables."""
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import JSON
from marshmallow import Schema, fields, post_load, post_dump

db = SQLAlchemy()

Column = db.Column
relationship = db.relationship

roles_users = db.Table(
    'roles_users',
    Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    """Simple role or database user."""

    id = Column(db.Integer(), primary_key=True)
    name = Column(db.String(80), unique=True)
    description = Column(db.String(255))


class User(db.Model, UserMixin):
    """User of proteomics database."""

    # __tablename__ = 'user_list'
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(255), unique=True)
    password = Column(db.String(255))
    active = Column(db.Boolean())
    confirmed_at = Column(db.DateTime())
    meta = Column(JSON)
    roles = relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


class Experiment(db.Model):
    """Holds experimental metadata."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    date = Column(db.DateTime())
    user_id = Column(db.Integer, db.ForeignKey('user.id'))
    organism_id = Column(db.Integer, db.ForeignKey('organism.id'))
    experiment_type_id = Column(db.Integer, db.ForeignKey('experiment_type.id'))
    probe_id = Column(db.Integer, db.ForeignKey('probe.id'))
    inhibitor_id = Column(db.Integer, db.ForeignKey('inhibitor.id'))
    additional_search_params = Column(JSON)
    additional_quant_params = Column(JSON)
    annotations = Column(JSON)
    # bidirectional many-to-one relationships corresponding to foreign keys above
    user = relationship('User', backref='experiments')
    organism = relationship('Organism', backref='experiments')
    experiment_type = relationship('ExperimentType', backref='experiments')
    probe = relationship('Probe', backref='experiments')
    inhibitor = relationship('Inhibitor', backref='experiments')


class JSONField(fields.Field):
    """Custom Field for handling Postgres' JSON data type."""

    def _serialize(self, value, attr, obj):
        if value is None:
            return ''
        return value

    def _deserialize(self, value, attr, data):
        return value


class ExperimentSchema(Schema):
    """Marshmallow schema for Experiement."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    date = fields.DateTime()
    user_id = fields.Integer()
    organism_id = fields.Integer()
    organism = fields.Nested('OrganismSchema')
    experiment_type_id = fields.Integer()
    experiment_type = fields.Nested('ExperimentTypeSchema')
    probe_id = fields.Integer()
    probe = fields.Nested('ProbeSchema')
    inhibitor_id = fields.Integer()
    inhibitor = fields.Nested('InhibitorSchema')
    additional_search_params = fields.String()
    additional_quant_params = fields.String()
    annotations = fields.String()

    @post_load
    def _make_experiment(self, data):
        return Experiment(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'experiments': data} if many else data


class Dataset(db.Model):
    """Holds actual experimental dataset."""

    __tablename__ = 'datasets'
    id = Column(db.Integer, primary_key=True)
    peptide_index = Column(db.Integer)
    ipi = Column(db.String(20))
    description = Column(db.Text)
    symbol = Column(db.String(20))
    sequence = Column(db.String(100))
    mass = Column(db.Numeric)
    charge = Column(db.Integer)
    segment = Column(db.Integer)
    ratio = Column(db.Numeric)
    intensity = Column(db.Numeric)
    num_ms2_peaks = Column(db.Integer)
    num_candidate_peaks = Column(db.Integer)
    max_light_intensity = Column(db.Numeric)
    light_noise = Column(db.Numeric)
    max_heavy_intensity = Column(db.Numeric)
    heavy_noise = Column(db.Numeric)
    rsquared = Column(db.Numeric)
    entry = Column(db.Integer)
    link = Column(db.String(100))
    discriminator = Column('experiment_id', db.Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'dataset',
        'polymorphic_on': discriminator
    }


class DatasetSchema(Schema):
    """Marshmallow schema for Dataset."""

    id = fields.Integer(dump_only=True)
    peptide_index = fields.Integer()
    ipi = fields.String()
    description = fields.String()
    symbol = fields.String()
    sequence = fields.String()
    mass = fields.Decimal()
    charge = fields.Integer()
    segment = fields.Integer()
    ratio = fields.Decimal()
    intensity = fields.Decimal()
    num_ms2_peaks = fields.Integer()
    num_candidate_peaks = fields.Integer()
    max_light_intensity = fields.Decimal()
    light_noise = fields.Decimal()
    max_heavy_intensity = fields.Decimal()
    heavy_noise = fields.Decimal()
    rsquared = fields.Decimal()
    entry = fields.Integer()
    link = fields.String()

    @post_dump(pass_many=True)
    def _wrap(self, data):
        return {'dataset': data}


class ExperimentType(db.Model):
    """Defines different experiment types."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    search_params = Column(JSON)
    cimage_params = Column(JSON)


class ExperimentTypeSchema(Schema):
    """Marshmallow schema for ExperimentType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'experiment_types': data} if many else data


class Organism(db.Model):
    """Holds data related to model organisms."""

    id = Column(db.Integer, primary_key=True)
    tax_id = Column(db.Integer)
    name = Column(db.String(80))
    display_name = Column(db.String(80))


class OrganismSchema(Schema):
    """Marshmallow schema for Organism."""

    id = fields.Integer(dump_only=True)
    tax_id = fields.Integer()
    name = fields.String()
    display_name = fields.String()

    @post_load
    def _make_organism(self, data):
        return Organism(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'organisms': data} if many else data


class Probe(db.Model):
    """Holds data about a particular probe."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    iupac_name = Column(db.Text)
    inchi = Column(db.Text)


class ProbeSchema(Schema):
    """Marshmallow schema for Probe."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    iupac_name = fields.String()
    inchi = fields.String()

    @post_load
    def _make_probe(self, data):
        return Probe(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'probes': data} if many else data


class Inhibitor(db.Model):
    """Holds data about a particular inhibitor."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    iupac_name = Column(db.Text)
    inchi = Column(db.Text)


class InhibitorSchema(Schema):
    """Marshmallow schema for Inhibitor."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    iupac_name = fields.String()
    inchi = fields.String()

    @post_load
    def _make_inhibitor(self, data):
        return Inhibitor(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'inhibitors': data} if many else data
