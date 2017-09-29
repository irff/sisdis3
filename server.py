from flask import Flask
from flask import request, jsonify
from datetime import datetime
import requests
import json

app = Flask(__name__)

STATE_URL = 'http://localhost:17088/'

def get_count(name):
    with open('data.json', "r+") as dbfile:
        content = json.load(dbfile)
        name_count = int(content.get(name, '0')) + 1

        content[name] = name_count

        dbfile.seek(0)
        dbfile.truncate()
        json.dump(content, dbfile)
        return name_count


@app.route('/api/hello', methods=['POST'])
def hello():
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

    return jsonify(response)

@app.route('/api/plus_one')
def plus_one():
    return 'Hello, World!'

