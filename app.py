from flask import Flask, render_template, jsonify, request
from crawling import server_restart

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    server_restart()
    app.run('0.0.0.0', port=5000, debug=True)
