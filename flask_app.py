
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template

from chat_app import add_chat_app_to


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


# simple chat app
add_chat_app_to(app)



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
    <p>Hier ist Musik: <audio src="https://upload.wikimedia.org/wikipedia/commons/a/a4/Oil_boiling.ogg" controls autoplay loop>Leider funktioniert Audio nicht</audio> -- sie sollte eigentlich automatisch starten, aber das scheint nicht immer zu funktionieren...</p>
    <p>Normaler Text -- kann auch länger sein...</p>
    <p>Sende Daten via POST</p>
    <form method="post" action="/greet_by_name">
      <input type="text" name="eingegebener_name" />
      <input type="date" />
      <input type="submit" value="Begrüße mich mit Namen" />
    </form>
    <p>Sende Daten via GET</p>
    <form method="get" action="/greet_by_name">
      <input type="text" name="eingegebener_name" />
      <input type="date" />
      <input type="submit" value="Begrüße mich mit Namen" />
    </form>
    <img alt="Konzert am Lichtenstern" src="https://www.evlgs.de/fileadmin/_processed_/f/5/csm_Musik_0c882e0401.jpg" />  <!-- hier wird <img> nicht durch ein </img> geschlossen, stattdessen schreiben wir <img/>, weil der Inhalt des Bildes schon im <img/> enthalten ist und nicht noch zwischen <img> und </img> eingerahmt werden muss. -->
    <p>Hier ein Link: <a href="https://www.google.de/">Hier kann man Google fragen...</a></p>
    <p>Hier ein Gif:</p>
    <img src="https://media.giphy.com/media/S99cgkURVO62qemEKM/giphy.gif" />
    <p>Und hier als <code>iframe</code>:</p>
    <iframe src="https://giphy.com/embed/S99cgkURVO62qemEKM" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    <p>Hier noch was spannendes zu Arduino-Projekten:</p>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/9ItEPmwfBqg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  </body>
</html>
"""


@app.route("/greet_by_name", methods=["GET", "POST"])
def greet_by_name():
    name = request.values.get("eingegebener_name")
    # see https://stackoverflow.com/a/20341272/2165903
    return render_template("greet_by_name.html", name=name)


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
