from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from crawling import collect_reset
import random

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.toyProject


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/data/data-reset', methods=['GET'])
def data_reset():
    return jsonify({'msg': collect_reset()})


@app.route('/api/data/all', methods=['GET'])
def show_data():
    data = list(db.client.toyProject.data.find({}, {'_id': False}))
    random.shuffle(data)
    return jsonify({'data': data})


@app.route('/api/data/drama', methods=['GET'])
def show_drama():
    drama = list(db.client.toyProject.data.find({'name': 'drama'}, {'_id': False}))
    random.shuffle(drama)
    return jsonify({'data': drama})


@app.route('/api/data/entertainment', methods=['GET'])
def show_entertainment():
    entertainment = list(db.client.toyProject.data.find({'name': 'entertainment'}, {'_id': False}))
    random.shuffle(entertainment)
    return jsonify({'data': entertainment})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
