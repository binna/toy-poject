from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from crawling import collect_reset
import random

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.toyProject


def get_random(num, start, end):
    cnt = 0
    a_dict = {}
    while True:
        if cnt == num:
            return list(a_dict.keys())

        num_created = random.randint(start, end)
        if num_created in a_dict:
            continue
        else:
            a_dict[num_created] = True
            cnt = cnt + 1


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/data-reset', methods=['GET'])
def data_reset():
    return jsonify({'msg': collect_reset()})


@app.route('/api/data', methods=['GET'])
def show_data():
    data = list(db.client.toyProject.data.find({}, {'_id': False}))
    random.shuffle(data)
    return jsonify({'data': data})


@app.route('/api/drama', methods=['GET'])
def show_drama():
    drama = list(db.client.toyProject.data.find({'name': 'drama'}, {'_id': False}))
    random.shuffle(drama)
    return jsonify({'drama': drama})

@app.route('/api/entertainment', methods=['GET'])
def show_entertainment():
    entertainment = list(db.client.toyProject.data.find({'name': 'entertainment'}, {'_id': False}))
    random.shuffle(entertainment)
    return jsonify({'entertainment': entertainment})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)