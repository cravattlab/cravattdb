"""Run the app with failsafe to prevent server from dying on syntax error."""
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from flask_failsafe import failsafe


@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from cravattdb import app
    return app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', threaded=True, port=5000))

if __name__ == '__main__':
    manager.run()
