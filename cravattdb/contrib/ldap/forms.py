"""Provides Flask-Security login forms for usage with LDAP auth backend."""

from werkzeug.local import LocalProxy
from flask import request, current_app
from flask_security.utils import encrypt_password
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_security.forms import Form, NextFormMixin, get_form_field_label
from flask_security.utils import config_value, get_message

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


class LDAPLoginForm(Form, NextFormMixin):
    """Login form for LDAP users."""

    email = StringField('User ID')
    password = PasswordField(get_form_field_label('password'))
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))

    def __init__(self, *args, **kwargs):
        """Init new LDAP login form."""
        super(LDAPLoginForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', '')
        self.remember.default = config_value('DEFAULT_REMEMBER_ME')

    def validate(self):
        """Validate LDAP logins against AD."""
        if not super(LDAPLoginForm, self).validate():
            return False

        if self.email.data.strip() == '':
            self.email.errors.append(get_message('USERID_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(
                get_message('PASSWORD_NOT_PROVIDED')[0]
            )
            return False

        user_dn, ldap_data = _datastore.query_ldap_user(self.email.data)

        if user_dn is None:
            self.email.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False

        if not _datastore.verify_password(user_dn, self.password.data):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False

        ldap_email = ldap_data.get(config_value('LDAP_EMAIL_FIELDNAME'), '')
        ldap_email = ldap_email[0].decode('utf-8')
        password = encrypt_password(self.password.data)

        if _datastore.find_user(email=ldap_email):
            self.user = _datastore.get_user(ldap_email)
            self.user.password = password
        else:
            self.user = _datastore.create_user(email=ldap_email, password=password)
            _datastore.commit()
        return True
