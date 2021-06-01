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

# test
@app.route('/api/get_watcha', methods=['GET'])
def watcha_get_four():
    watcha = list(db.client.toyProject.watcha.find({}, {'_id': False}))
    keys = get_random(4, 0, 47)
    random_watcha = []
    for key in keys:
        random_watcha.append(watcha[key])
    return jsonify({'random_watcha': random_watcha})


@app.route('/api/get_wavve', methods=['GET'])
def wavve_get_four():
    wavve = list(db.client.toyProject.wavve.find({}, {'_id': False}))
    keys = get_random(4, 0, 50)
    random_wavve = []
    for key in keys:
        random_wavve.append(wavve[key])
    return jsonify({'random_wavve': random_wavve})



@app.route('/api/wavve_drama', methods=['GET'])
def wavve_get_drama():
    wavve_drama = list(db.client.toyProject.wavve.find({'name': 'drama'}, {'_id': False}))
    return jsonify({'wavve_drama': wavve_drama})

@app.route('/api/watcha_drama', methods=['GET'])
def watcha_get_drama():
    watcha_drama = list(db.client.toyProject.watcha.find({'name': 'drama'}, {'_id': False}))
    return jsonify({'watcha_drama': watcha_drama})


@app.route('/api/wavve_entertainment', methods=['GET'])
def wavve_get_entertainment():
    wavve_entertainment = list(db.client.toyProject.wavve.find({'name': 'entertainment'}, {'_id': False}))
    return jsonify({'wavve_entertainment': wavve_entertainment})

@app.route('/api/watcha_entertainment', methods=['GET'])
def watcha_get_entertainment():
    watcha_entertainment = list(db.client.toyProject.watcha.find({'name': 'entertainment'}, {'_id': False}))
    return jsonify({'watcha_entertainment': watcha_entertainment})



# TODO 처음 데이터 받아오는 api (예능 + 드라마), 추천 드라마
# TODO 예능 눌렀을때 예능 데이터만 받아오는 api
# TODO 드라마 눌렀을때 예능 데이터만 받아오는 api
# TODO 확인 버튼 눌렀을때 api


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


