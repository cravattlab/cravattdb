"""User models."""
from cravattdb import db
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import JSON

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
