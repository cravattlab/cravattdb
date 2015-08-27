import os
import config.config as config
from flask import Flask, render_template, jsonify, request, abort, make_response
from models.search import Search
from models.upload import Upload
import models.convert as convert
import models.quantify as quantify

app = Flask(__name__)
app.debug = True

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
    path = os.path.join(username, name)
    Upload(request.files.getlist('file'), path)

    # convert .raw to .ms2
    convert_status = convert.convert(path)

    files = []

    for f in convert_status['files_converted']:
        files.append(os.path.join(config.UPLOAD_FOLDER, path, f))

    # initiate IP2 search
    dta_select_link = search.search(
        request.form.get('organism'),
        request.form.get('experiment_type'),
        [ f for f in files if f.endswith('.ms2') ]
    )

    # quantify all of the things
    quantify.quantify(
        name,
        dta_select_link,
        request.form.get('experiment_type'),
        os.path.join(username, name)
    )

    return 'hello'

@app.route('/status', methods = [ 'GET' ])
def status():
    return render_template('index.html')

def error_response(details, code):
    return make_response(jsonify({ 'error': details }), code)

@app.errorhandler(401)
def unauthorized(error):
    return error_response(error.description, error.code)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)