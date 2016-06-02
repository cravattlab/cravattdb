"""Patch mail to ehlo le server."""
import flask_mail
import smtplib


class _Connection(flask_mail.Connection):
    def configure_host(self):
        if self.mail.use_ssl:
            host = smtplib.SMTP_SSL(self.mail.server, self.mail.port)
        else:
            host = smtplib.SMTP(self.mail.server, self.mail.port)

        host.set_debuglevel(int(self.mail.debug))

        if self.mail.use_tls:
            host.starttls()
            host.ehlo()
        if self.mail.username and self.mail.password:
            host.login(self.mail.username, self.mail.password)

        return host

flask_mail.Connection = _Connection

Mail = flask_mail.Mail
