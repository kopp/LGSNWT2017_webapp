
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Titel</title>
  </head>
  <body>
    <h1>Überschrift</h1>
    <h2>kleinere Überschrift</h2>
    <p>Normaler Text -- kann auch länger sein...</p>
    <img alt="Konzert am Lichtenstern" src="https://www.evlgs.de/fileadmin/_processed_/f/5/csm_Musik_0c882e0401.jpg" />  <!-- hier wird <img> nicht durch ein </img> geschlossen, stattdessen schreiben wir <img/>, weil der Inhalt des Bildes schon im <img/> enthalten ist und nicht noch zwischen <img> und </img> eingerahmt werden muss. -->
    <p>Hier ein Link: <a href="https://www.google.de/">Hier kann man Google fragen...</a></p>
    <form>
      <input type="text" />
      <input type="date" />
      <input type="submit" />
    </form>
  </body>
</html>
"""


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