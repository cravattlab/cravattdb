from flask import Flask, render_template, jsonify, request, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required
from models.search import Search
from models.tasks import process
from models.database import db
import models.upload as upload
import config.config as config
import models.user as user

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

# Create database connection object
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, user.User, user.Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<name>', methods = [ 'POST' ])
def search(name):
    username = request.form.get('username')

    search = Search(name)

    login = search.login(
        request.form.get('username'),
        request.form.get('password')
    )

    if not login: abort(401)

    # save RAW files to disk
    # path is type pathlib.Path
    try:
        name, path = upload.upload(
            request.files.getlist('file'),
            username,
            name
        )
    except FileExistsError:
        abort(409)

    # continue processing in background with celery
    process.delay(
        search,
        name, 
        path,
        request.form.get('organism'),
        request.form.get('experiment_type')
    )

    return 'hello'

@app.route('/status', methods = [ 'GET' ])
@login_required
def status():
    return render_template('index.html')

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db.session.commit()

def error_response(details, code):
    return make_response(jsonify({ 'error': details }), code)

@app.errorhandler(401)
def unauthorized(error):
    return error_response(error.description, error.code)

@app.errorhandler(409)
def dataset_exists(error):
    return error_response(error.description, error.code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)