import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

client = MongoClient('ec2-18-163-75-126.ap-east-1.compute.amazonaws.com', 27017)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Flask API for writing to Mongo DB on EC2!"

@app.route('/add', methods=['POST'])
def add_message():
    try:
        _json = request.json
        _author = _json['author']
        _message = _json['message']
        db = client['flaskApi']
        writer = db['api1']
        payload = {
            'author': _author,
            'message': _message
        }
        writer.insert_one(payload)
        resp = jsonify('message recorded')
        resp.status_code = 200
        return resp
    except Exception as e:
        return e

@app.route('/from/<author>')
def show_message(author):
    db = client['flaskApi']
    writer = db['api1']
    messages = writer.find({"author":author})
    resp = {
        'author': author,
        'messages': []
    }
    for msg in messages:
        resp['messages'].append(msg['message'])
    return json.dumps(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
