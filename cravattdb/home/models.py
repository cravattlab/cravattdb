"""Contains definitions of SQLAlchemy tables."""
from sqlalchemy.dialects.postgresql import JSON, JSONB
from marshmallow import Schema, fields, pre_load, post_load, post_dump, validate
from cravattdb.users.models import UserSchema
from cravattdb.utils.admin import AuthModelView
from cravattdb import db, admin

Column = db.Column
relationship = db.relationship


class Experiment(db.Model):
    """Holds experimental metadata."""

    __tablename__ = 'experiment'

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
    sample_type_id = Column(db.Integer, db.ForeignKey('sample_type.id'), index=True)
    cell_type_id = Column(db.Integer, db.ForeignKey('cell_type.id'), index=True)
    instrument_id = Column(db.Integer, db.ForeignKey('instrument.id'), index=True)
    proteomic_fraction_id = Column(db.Integer, db.ForeignKey('proteomic_fraction.id'), index=True)

    # store search and quantification parameter data
    search_params = Column(JSONB)
    quant_params = Column(JSONB)

    annotations = Column(JSONB)

    # datasets can be quantified as Heavy/Light or Light/Heavy
    # necessary due to cimage returning different results for H/L vs L/H
    # it is sometimes desirable to switch between H/L and L/H
    ratio_numerator = Column(db.Enum('L', 'H', name='ratio_numerator_types'), index=True)

    # reference to dataset that is inversely quantified
    inverse_ratio_id = Column(db.Integer, db.ForeignKey('experiment.id'), index=True)

    # set if this dataset is a replicate of another
    replicate_of = Column(db.Integer, db.ForeignKey('experiment.id'), index=True)

    # whether or not dataset should be publicly accessible
    public = Column(db.Boolean)

    # bidirectional many-to-one relationships corresponding to foreign keys above
    user = relationship('User', backref='experiments')
    organism = relationship('Organism', backref='experiments')
    experiment_type = relationship('ExperimentType', backref='experiments')
    sample_type = relationship('SampleType', backref='experiments')
    cell_type = relationship('CellType', backref='experiments')
    instrument = relationship('Instrument', backref='experiments')
    proteomic_fraction = relationship('ProteomicFraction', backref='experiments')
    replicates = relationship('Experiment', foreign_keys=[replicate_of])
    inverted_dataset = relationship('Experiment', foreign_keys=[inverse_ratio_id])
    treatments = relationship('Treatment', backref='experiment')


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
    name = fields.String(required=True)
    date = fields.DateTime()
    modified = fields.DateTime()
    user_id = fields.Integer(required=True)
    user = fields.Nested('UserSchema', dump_only=True)
    organism_id = fields.Integer()
    organism = fields.Nested('OrganismSchema', dump_only=True)
    experiment_type_id = fields.Integer(load_only=True)
    experiment_type = fields.Nested('ExperimentTypeSchema', dump_only=True)
    sample_type_id = fields.Integer(load_only=True)
    sample_type = fields.Nested('SampleTypeSchema', dump_only=True)
    cell_type_id = fields.Integer(load_only=True)
    cell_type = fields.Nested('CellTypeSchema', dump_only=True)
    instrument_id = fields.Integer(load_only=True)
    instrument = fields.Nested('InstrumentSchema', dump_only=True)
    proteomic_fraction_id = fields.Integer(load_only=True)
    proteomic_fraction = fields.Nested('ProteomicFractionSchema', dump_only=True)
    search_params = JSONField()
    quant_params = JSONField()
    treatments = fields.Nested('TreatmentSchema', dump_only=True, many=True)
    annotations = JSONField()
    ratio_numerator = fields.String()
    replicate_of = fields.Integer()
    inverse_ratio_id = fields.Integer()
    public = fields.Boolean()

    @pre_load
    def _filter_experiment(self, data):
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def _make_experiment(self, data):
        return Experiment(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'experiments': data} if many else data


class Treatment(db.Model):
    """Describes types of treatment applied to a proteome in an experiment."""

    id = Column(db.Integer, primary_key=True)
    experiment_id = Column(db.Integer, db.ForeignKey('experiment.id'), index=True)
    description = Column(db.Text)
    method = Column(db.Enum('in vitro', 'in vivo', 'in situ', name='method_types'), index=True)
    fraction = Column(db.Enum('L', 'H', name='fraction_types'), index=True)

    # treatment time in hours
    time = Column(db.Numeric)

    # concentration in micromoles
    concentration = Column(db.Numeric)

    # the most common treatments are with inhibitors or probes
    # only one of inhibitor_id, probe_id, or other should be set per row
    inhibitor_id = Column(db.Integer, db.ForeignKey('inhibitor.id'), index=True)
    probe_id = Column(db.Integer, db.ForeignKey('probe.id'), index=True)
    # for storing other type of treatments
    other = Column(db.Text)

    inhibitor = relationship('Inhibitor', backref='treatments')
    probe = relationship('Probe', backref='treatments')


class TreatmentSchema(Schema):
    """Marshmallow schema for Treatment."""

    id = fields.Integer(dump_only=True)
    experiment_id = fields.Integer(load_only=True)
    description = fields.String()
    method = fields.String()
    fraction = fields.String()
    time = fields.Float()
    concentration = fields.Float()
    inhibitor_id = fields.Integer(load_only=True)
    inhibitor = fields.Nested('InhibitorSchema', dump_only=True)
    probe_id = fields.Integer(load_only=True)
    probe = fields.Nested('ProbeSchema', dump_only=True)
    other = fields.String()

    @post_load
    def _make_treatment(self, data):
        return Treatment(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return data


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
    name = Column(db.Text, index=True, unique=True)
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
    name = Column(db.Text, index=True, unique=True)
    tax_id = Column(db.Integer, unique=True)
    scientific_name = Column(db.Text, index=True, unique=True)


class OrganismSchema(Schema):
    """Marshmallow schema for Organism."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    tax_id = fields.Integer(allow_none=True)
    scientific_name = fields.String(allow_none=True)

    @post_load
    def _make_organism(self, data):
        return Organism(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'organisms': data} if many else data


class Probe(db.Model):
    """Holds data about a particular probe."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)
    iupac_name = Column(db.Text, index=True, unique=True)
    inchi = Column(db.Text, index=True, unique=True)


class ProbeSchema(Schema):
    """Marshmallow schema for Probe."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    iupac_name = fields.String(allow_none=True)
    inchi = fields.String(allow_none=True)

    @post_load
    def _make_probe(self, data):
        return Probe(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'probes': data} if many else data


class Inhibitor(db.Model):
    """Holds data about a particular inhibitor."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)
    iupac_name = Column(db.Text, index=True, unique=True)
    inchi = Column(db.Text, index=True, unique=True)


class InhibitorSchema(Schema):
    """Marshmallow schema for Inhibitor."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    iupac_name = fields.String(allow_none=True)
    inchi = fields.String(allow_none=True)

    @post_load
    def _make_inhibitor(self, data):
        return Inhibitor(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'inhibitors': data} if many else data


class Instrument(db.Model):
    """Describes mass spec instruments."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)


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


class SampleType(db.Model):
    """Define sample types such as tissue, cell, etc."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)
    description = Column(db.Text)


class SampleTypeSchema(Schema):
    """Marshmallow schema for SampleType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)

    @post_load
    def _make_sample_type(self, data):
        return SampleType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'sample_types': data} if many else data


class CellType(db.Model):
    """Define type of cells used in experiment. Can be cell line or primary cell type."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)
    description = Column(db.Text, index=True)


class CellTypeSchema(Schema):
    """Marshmallow schema for CellType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)

    @post_load
    def _make_cell_type(self, data):
        return CellType(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'cell_types': data} if many else data


class ProteomicFraction(db.Model):
    """Define proteome fraction: soluble, membrane etc."""

    id = Column(db.Integer, primary_key=True)
    name = Column(db.Text, index=True, unique=True)
    description = Column(db.Text, index=True)


class ProteomicFractionSchema(Schema):
    """Marshmallow schema for CellType."""

    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String(allow_none=True)

    @post_load
    def _make_proteomic_fraction(self, data):
        return ProteomicFraction(**data)

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'proteomic_fractions': data} if many else data


# Flask-Admin views defined here for convenience
admin.add_view(AuthModelView(Probe, db.session))
admin.add_view(AuthModelView(Dataset, db.session))
admin.add_view(AuthModelView(Inhibitor, db.session))
admin.add_view(AuthModelView(Experiment, db.session))
admin.add_view(AuthModelView(ExperimentType, db.session))
admin.add_view(AuthModelView(Organism, db.session))
admin.add_view(AuthModelView(SampleType, db.session))
admin.add_view(AuthModelView(CellType, db.session))
admin.add_view(AuthModelView(Instrument, db.session))
admin.add_view(AuthModelView(ProteomicFraction, db.session))
