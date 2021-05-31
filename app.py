from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from crawling import collect_reset

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.toyProject


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/data-reset', methods=['GET'])
def data_reset():
    return jsonify({'msg': collect_reset()})

# TODO 처음 데이터 받아오는 api (예능 + 드라마), 추천 드라마
# TODO 예능 눌렀을때 예능 데이터만 받아오는 api
# TODO 드라마 눌렀을때 예능 데이터만 받아오는 api
# TODO 확인 버튼 눌렀을때 api


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
