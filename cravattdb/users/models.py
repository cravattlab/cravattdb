"""User models."""
from flask_security import UserMixin, RoleMixin
from cravattdb.utils.admin import AuthModelView
from marshmallow import Schema, fields, post_dump
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property
from cravattdb import db, admin

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

    @hybrid_property
    def username(self):
        print('hello', self.email)
        return self.email.split('@')[0]

    @username.expression
    def username(cls):
        return func.split_part(cls.email, '@', 1)



class UserSchema(Schema):
    """Marshmallow schema for User."""

    id = fields.Integer(dump_only=True)
    email = fields.String(dump_only=True)
    name = fields.Function(lambda obj: obj.email.split('@')[0])

    @post_dump(pass_many=True)
    def _wrap(self, data, many):
        return {'users': data} if many else data


# Flask-Admin views defined here for convenience
admin.add_view(AuthModelView(User, db.session))
admin.add_view(AuthModelView(Role, db.session))
