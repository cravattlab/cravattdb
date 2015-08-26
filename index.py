import os
from flask import Flask, render_template, jsonify, request, abort, make_response
from models.search import Search
from models.upload import Upload
from functools import partial
import models.convert as convert

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

    # convert to .ms2 and start ip2 search when done
    convert.convert(path, 
        partial(
            search.search,
            request.form.get('organism'),
            request.form.get('experiment_type'),
            path
        )
    )

    # quantify all of the things

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