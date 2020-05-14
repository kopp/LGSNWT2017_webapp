
# A very simple Flask Hello World app for you to get started with...

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hallo " + adee()

@app.route('/adee')
def adee():
    return "adee"


n = 1

@app.route('/add')
def add():
    global n
    n = n + 1
    return str(n)

@app.route('/sub')
def sub():
    global n
    n = n - 1
    return str(n)

@app.route('/get')
def get():
    return str(n)