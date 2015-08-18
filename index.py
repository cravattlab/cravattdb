from flask import Flask, render_template, jsonify, request
from models.search import Search

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<name>', methods = [ 'POST' ])
def search(name):
    search = Search()

    search.login(
        request.json['username'],
        request.json['password']
    )

    search.search(
        request.files,
        request.json['organism'],
        request.json['experiment_type'],
        request.json['param_mods']
    )

    return jsonify(request.json)

if __name__ == "__main__":
    app.run(host='0.0.0.0')