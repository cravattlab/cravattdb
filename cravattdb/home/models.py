"""Contains definitions of SQLAlchemy tables."""
from sqlalchemy.dialects.postgresql import JSON, JSONB
from marshmallow import Schema, fields, pre_load, post_load, post_dump
from cravattdb.users.models import UserSchema
from cravattdb.utils.admin import AuthModelView
from cravattdb import db, admin

Column = db.Column
relationship = db.relationship


class Experiment(db.Model):
    """Holds experimental metadata."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text)
    description = Column(db.Text)

    # creation date
    date = Column(db.DateTime())
    # modification time
    modified = Column(db.DateTime())

    user_id = Column(db.Integer, db.ForeignKey('user.id'), index=True)
    organism_id = Column(db.Integer, db.ForeignKey('organism.id'), index=True)
    experiment_type_id = Column(db.Integer, db.ForeignKey('experiment_type.id'), index=True)
    probe_id = Column(db.Integer, db.ForeignKey('probe.id'), index=True)
    inhibitor_id = Column(db.Integer, db.ForeignKey('inhibitor.id'), index=True)

    sample_type_id = Column(db.Integer, db.ForeignKey('sample_type.id'), index=True)
    cell_type_id = Column(db.Integer, db.ForeignKey('cell_type.id'), index=True)
    instrument_id = Column(db.Integer, db.ForeignKey('instrument.id'), index=True)
    treatment_type_id = Column(db.Integer, db.ForeignKey('treatment_type.id'), index=True)

    # store things like concentration, duration etc
    treatment_details = Column(JSONB)

    # store overrides for parameters
    additional_search_params = Column(JSON)
    additional_quant_params = Column(JSON)

    annotations = Column(JSON)

    # bidirectional many-to-one relationships corresponding to foreign keys above
    user = relationship('User', backref='experiments')
    organism = relationship('Organism', backref='experiments')
    experiment_type = relationship('ExperimentType', backref='experiments')
    probe = relationship('Probe', backref='experiments')
    inhibitor = relationship('Inhibitor', backref='experiments')
    sample_type = relationship('SampleType', backref='experiments')
    cell_type = relationship('CellType', backref='experiments')
    instrument = relationship('Instrument', backref='experiments')
    treatment_type = relationship('TreatmentType', backref='experiments')


class JSONField(fields.Field):
    """Custom Field for handling Postgres' JSON data type."""

    def _serialize(self, value, attr, obj):
        if value is None:
            return ''
        return value

    def _deserialize(self, value, attr, data):
        return value


class ExperimentSchema(Schema):
    """Marshmallow schema for Experiment."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    date = fields.DateTime()
    user = fields.Nested('UserSchema')
    organism = fields.Nested('OrganismSchema')
    experiment_type = fields.Nested('ExperimentTypeSchema')
    probe = fields.Nested('ProbeSchema')
    inhibitor = fields.Nested('InhibitorSchema')
    sample_type = fields.Nested('SampleType')
    cell_type = fields.Nested('CellType')
    instrument = fields.Nested('Instrument')
    treatment_type = fields.Nested('TreatmentType')
    additional_search_params = JSONField()
    additional_quant_params = JSONField()
    treatmentDetails = JSONField()
    annotations = JSONField()

    @pre_load
    def _filter_experiment(self, data):
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def _make_experiment(self, data):
        return Experiment(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'experiments': data} if many else data


class Dataset(db.Model):
    """Holds actual experimental dataset."""

    id = Column(db.Integer, primary_key=True)
    peptide_index = Column(db.Integer)
    uniprot = Column(db.Text, index=True)
    description = Column(db.Text, index=True)
    symbol = Column(db.Text, index=True)
    sequence = Column(db.Text, index=True)
    clean_sequence = Column(db.Text, index=True)
    mass = Column(db.Numeric)
    charge = Column(db.Integer)
    segment = Column(db.Integer)
    ratio = Column(db.Numeric, index=True)
    intensity = Column(db.Numeric)
    num_ms2_peaks = Column(db.Integer)
    num_candidate_peaks = Column(db.Integer)
    max_light_intensity = Column(db.Numeric)
    light_noise = Column(db.Numeric)
    max_heavy_intensity = Column(db.Numeric)
    heavy_noise = Column(db.Numeric)
    rsquared = Column(db.Numeric)
    entry = Column(db.Integer)
    experiment_id = Column(db.Integer, db.ForeignKey('experiment.id'), index=True)


class DatasetSchema(Schema):
    """Marshmallow schema for Dataset."""

    id = fields.Integer(dump_only=True)
    peptide_index = fields.Integer()
    uniprot = fields.String()
    description = fields.String()
    symbol = fields.String()
    sequence = fields.String()
    mass = fields.Float()
    charge = fields.Integer()
    segment = fields.Integer()
    ratio = fields.Float()
    intensity = fields.Float()
    num_ms2_peaks = fields.Integer()
    num_candidate_peaks = fields.Integer()
    max_light_intensity = fields.Float()
    light_noise = fields.Float()
    max_heavy_intensity = fields.Float()
    heavy_noise = fields.Float()
    rsquared = fields.Float()
    entry = fields.Integer()
    link = fields.String()
    experiment_id = fields.Integer()

    class Meta:
        """Additional settings."""

        ordered = True

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'dataset': data}


class ExperimentType(db.Model):
    """Defines different experiment types."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True)
    search_params = Column(JSON)
    cimage_params = Column(JSON)


class ExperimentTypeSchema(Schema):
    """Marshmallow schema for ExperimentType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()

    @post_load
    def _make_experiment_type(self, data):
        return ExperimentType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'experiment_types': data} if many else data


class Organism(db.Model):
    """Holds data related to model organisms."""

    id = Column(db.Integer, primary_key=True)
    tax_id = Column(db.Integer)
    name = Column(db.Text, index=True)
    display_name = Column(db.Text, index=True)


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
    name = Column(db.Text, index=True)
    iupac_name = Column(db.Text, index=True)
    inchi = Column(db.Text, index=True)


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
    name = Column(db.Text, index=True)
    iupac_name = Column(db.Text, index=True)
    inchi = Column(db.Text, index=True)


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


class Instrument(db.Model):
    """Describes mass spec instruments."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True)


class InstrumentSchema(Schema):
    """Marshmallow schema for Instrument."""

    id = fields.Integer(dump_only=True)
    name = fields.String()

    @post_load
    def _make_instrument(self, data):
        return Instrument(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'instruments': data} if many else data


class TreatmentType(db.Model):
    """Type of treatment applied to proteome: in vitro etc."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True)
    description = Column(db.Text)


class TreatmentTypeSchema(Schema):
    """Marshmallow schema for TreatmentType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()

    @post_load
    def _make_treatment_type(self, data):
        return TreatmentType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'treatment_types': data} if many else data


class SampleType(db.Model):
    """Define sample types such as tissue, cell, etc."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True)
    description = Column(db.Text)


class SampleTypeSchema(Schema):
    """Marshmallow schema for SampleType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()

    @post_load
    def _make_sample_type(self, data):
        return SampleType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'sample_types': data} if many else data


class CellType(db.Model):
    """Define type of cells used in experiment. Can be cell line or primary cell type."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Integer, index=True)
    description = Column(db.Text, index=True)


class CellTypeSchema(Schema):
    """Marshmallow schema for CellType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()

    @post_load
    def _make_cell_type(self, data):
        return CellType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'cell_types': data} if many else data

# Flask-Admin views defined here for convenience
admin.add_view(AuthModelView(Probe, db.session))
admin.add_view(AuthModelView(Dataset, db.session))
admin.add_view(AuthModelView(Inhibitor, db.session))
admin.add_view(AuthModelView(Experiment, db.session))
admin.add_view(AuthModelView(ExperimentType, db.session))
admin.add_view(AuthModelView(Organism, db.session))
