from flask import Flask, render_template, jsonify, request
from models.search import Search

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<name>', methods = [ 'POST' ])
def search(name):
    search = Search(name)

    search.login(
        request.form['username'],
        request.form['password']
    )

    search.search(
        request.files,
        request.form['organism'],
        request.form['experiment_type'],
        request.form['param_mods']
    )

    return 'hello'

if __name__ == "__main__":
    app.run(host='0.0.0.0')