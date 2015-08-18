from flask import Flask, render_template, jsonify, request
from models.ip2 import IP2

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/<name>', methods = [ 'POST' ])
def search(name):
    test = {
        'test': 'wat'
    }

    ip2 = IP2(name)

    ip2.login(
        request.json['username'],
        request.json['password']
    )

    return jsonify(request.json)



if __name__ == "__main__":
    app.run(host='0.0.0.0')