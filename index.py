from flask import Flask, render_template, jsonify, request, abort, make_response
from models.search import Search

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<name>', methods = [ 'POST' ])
def search(name):
    search = Search(name)

    login = search.login(
        request.form.get('username'),
        request.form.get('password')
    )

    if not login: abort(401)

    search.search(
        request.files.getlist('file'),
        request.form.get('organism'),
        request.form.get('experiment_type'),
        request.form.get('param_mods')
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