"""Connects Flask-Security datastore to LDAP."""

import ldap
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import config_value


class LDAPUserDatastore(SQLAlchemyUserDatastore):
    """Provide datastore based on Flask Security's SQLAlchemyDatastore."""

    def __init__(self, db, user_model, role_model):
        """Init new datastore given user and role models."""
        SQLAlchemyUserDatastore.__init__(self, db, user_model, role_model)

    def _get_ldap_con(self):
        con = ldap.initialize(config_value('LDAP_URI'), bytes_mode=False)
        con.simple_bind_s(config_value('LDAP_BIND_DN'), config_value('LDAP_BIND_PASSWORD'))
        return con

    def _close_ldap_con(self, con):
        con.unbind_s()

    def query_ldap_user(self, identifier):
        """Get information about a user throught AD."""
        con = self._get_ldap_con()
        results = con.search_s(
            config_value('LDAP_BASE_DN'), ldap.SCOPE_SUBTREE,
            config_value('LDAP_SEARCH_FILTER').format(identifier)
        )
        self._close_ldap_con(con)
        if len(results) > 0:
            return results[0]
        else:
            return (None, None)

    def verify_password(self, user_dn, password):
        """Attempt to authenticate against AD."""
        con = self._get_ldap_con()
        valid = True
        try:
            con.simple_bind_s(user_dn, password)
        except ldap.INVALID_CREDENTIALS:
            valid = False
        self._close_ldap_con(con)
        return valid
