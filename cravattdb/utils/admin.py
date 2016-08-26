"""Patch Flask-Admin to require Flask-Security authentication."""
from flask_admin import AdminIndexView
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView


class _AuthBase:
    def is_accessible(self):
        """Verify that user is authenticated before rendering admin index."""
        return current_user.is_authenticated


class AuthAdminIndexView(_AuthBase, AdminIndexView):
    """Verify that user is authenticated before rendering admin index."""

    pass


class AuthModelView(_AuthBase, ModelView):
    """Verify that user is authenticated before rendering model view."""

    pass
