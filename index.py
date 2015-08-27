from pathlib import PurePath
from flask import Flask, render_template, jsonify, request, abort, make_response
from models.search import Search
from models.upload import Upload
import models.convert as convert
import models.quantify as quantify
import models.upload as upload

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
    # path is type pathlib.Path
    name, path = upload.upload(request.files.getlist('file'), username, name)

    # convert .raw to .ms2
    # removing first bit of file path since that is the upload folder
    convert_status = convert.convert(PurePath(path.parts[1:]).as_posix())

    converted_paths = [ path.joinpath(path, f) for f in convert_status['files_converted'] ]

    # initiate IP2 search
    dta_select_link = search.search(
        request.form.get('organism'),
        request.form.get('experiment_type'),
        [ f for f in converted_paths if f.suffix == '.ms2']
    )

    # quantify all of the things
    quantify.quantify(
        name,
        dta_select_link,
        request.form.get('experiment_type'),
        path
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