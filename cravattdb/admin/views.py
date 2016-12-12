"""Flask-admin view setup."""
from ..utils.admin import AuthModelView
from ..users.models import User, Role
from ..shared.models import (
    Probe,
    Dataset,
    Inhibitor,
    Experiment,
    ExperimentType,
    Organism,
    SampleType,
    CellType,
    Instrument,
    ProteomicFraction
)


def bootstrap_admin(admin, db):
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
    admin.add_view(AuthModelView(User, db.session))
    admin.add_view(AuthModelView(Role, db.session))
