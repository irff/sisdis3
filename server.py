from flask import Flask
from flask import request, jsonify
from datetime import datetime
import requests
import json

app = Flask(__name__)

STATE_URL = 'http://172.17.0.70:17088/'

def get_count(name):
    with open('data.json', "r+") as dbfile:
        content = json.load(dbfile)
        name_count = int(content.get(name, '0')) + 1

        content[name] = name_count

        dbfile.seek(0)
        dbfile.truncate()
        json.dump(content, dbfile)
        return name_count


@app.route('/api/hello', methods=['GET', 'POST'])
def hello():
    print request.method
    if request.method == 'POST':
        req = request.get_json()
        if req['request']:
            name = req['request']
            state = requests.get(STATE_URL).json()
            state_text = state['state']

            response = {
                "apiversion": 1,
                "count": get_count(name),
                "currentvisit": str(datetime.now()),
                "response": state_text + ', ' + name
            }

        else:
            response = {
                "detail": "'request' is a required property",
                "status": 400,
                "title": "Bad Request"
            }
    else:
        response = {
            "detail": "Method Not Allowed. Only POST is supported",
            "status": 405,
            "title": "Method Not Allowed"
        }

    return jsonify(response)


@app.route('/api/plus_one/<number>')
def plus_one(number=None):
    if request.method == 'GET':
        try:
            number = int(number)
            response = {
                "apiversion": 1,
                "plusoneret": number + 1
            }

        except ValueError:
            response = {
                "detail": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
                "status": 404,
                "title": "Not Found"
            }
    else:
        response = {
            "detail": "Method Not Allowed. Only GET is supported",
            "status": 405,
            "title": "Method Not Allowed"
        }

    return jsonify(response)

@app.route('/api/spesifikasi.yaml')
def spesifikasi():
    if request.method == 'GET':
        with open('spesifikasi.yaml', "r") as dbfile:
            return dbfile.read()
    else:
        response = {
            "detail": "Method Not Allowed. Only GET is supported",
            "status": 405,
            "title": "Method Not Allowed"
        }

    return jsonify(response)

@app.errorhandler(404)
def error_404(error):
    response = {
        "detail": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
        "status": 404,
        "title": "Not Found"
    }
    return jsonify(response)
