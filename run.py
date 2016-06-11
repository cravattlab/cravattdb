"""Run the app with failsafe to prevent server from dying on syntax error."""
from flask.ext.script import Server
from flask_failsafe import failsafe


@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from cravattdb import manager
    return manager

manager = create_app()
manager.add_command('runserver', Server(host='0.0.0.0', threaded=True, port=5000))

if __name__ == "__main__":
    manager.run()
