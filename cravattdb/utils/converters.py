"""Utility module for non-standard url converters."""

from werkzeug.routing import BaseConverter, ValidationError


class MatrixConverter(BaseConverter):
    """Provide conversion for matrix parameters.

    Lifted from Martijn Pieters
    http://stackoverflow.com/a/21060863/383744
    """

    def __init__(self, url_map, **defaults):
        super(MatrixConverter, self).__init__(url_map)
        self.defaults = {k: str(v) for k, v in defaults.items()}

    def to_dict(self, value):
        """Convert parametrs to dict."""
        if not value.startswith(';'):
            raise ValidationError()
        value = value[1:]
        parts = value.split(';')
        result = self.defaults.copy()
        for part in parts:
            try:
                key, value = part.split('=')
            except ValueError:
                raise ValidationError()
            result[key.strip()] = value.strip()
        return result

    def to_url(self, value):
        """Output url form of params."""
        return ';' + ';'.join('{}={}'.format(*item) for item in value.items())
