from flask import Flask
from flask import jsonify
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def hello():
    current_time = datetime.now()
    response = {
        'datetime': current_time,
        'state': 'Morning'
    }

    return jsonify(response)
