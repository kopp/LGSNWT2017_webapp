
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request


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

@app.route('/add_n', methods=["GET"])
def add_n():
    global n
    p_as_text = request.args.get('p')
    p_as_integer = int(p_as_text)
    n = n + p_as_integer
    return str(n)

@app.route('/sub')
def sub():
    global n
    n = n - 1
    return str(n)

@app.route('/get')
def get():
    return str(n)