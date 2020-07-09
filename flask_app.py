
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, render_template
from flask import redirect, url_for
from sql_helpers import execute_sql


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


# simple chat app

MySQL_DATABASE_CHAT_APP = "lgsnwt00$ChatApp"

ALLOW_SQL_INJECTIONS = True

@app.route("/chat")
@app.route("/chat/")
def chat_login_page():
    return """
    <h1>Login to this fancy chat</h1>
    <form action="/chat/login" method="POST">
      <label for="login_user">Username: </label>
      <input type="text" id="login_user" name="login_user" />
      <label for="login_password">Password: </label>
      <input type="password" id="login_password" name="login_password" />
      <input type="submit" />
    </form>
    <h1>Create account</h1>
    <form action="/chat/newaccount" method="POST">
      <label for="new_user">Username: </label>
      <input type="text" id="new_user" name="new_user" />
      <label for="new_password">Password: </label>
      <input type="password" id="new_password" name="new_password" />
      <input type="submit" />
    </form>
    """


@app.route("/chat/newaccount", methods=["POST"])
def chat_create_account():
    try:
        username = request.values["new_user"]
        password = request.values["new_password"]
        add_user(username, password)
        return """
        Account {} created -- <a href="{}">log in</a>.
        """.format(username, url_for("chat_login_page"))
    except:
        return "Problems when creating the account; sorry"


@app.route("/chat/login", methods=["POST"])
def chat_login():
    username = request.values["login_user"]
    password = request.values["login_password"]
    if not is_password_correct(username, password):
        return """
        Invalid password or unknown user {} -- please <a href="{}">try again</a>.
        """.format(username, url_for("chat_login_page"))
    user_id = get_user_id(username)
    if user_id is None:
        return """
        User {} is not known -- please <a href="{}">register first</a>.
        """.format(username, url_for("chat_login_page"))
    else:
        return redirect(url_for("chat_window", user_id=user_id))


@app.route("/chat/chat")
def chat_window():
    user_id = request.values["user_id"]
    show_all_messages = bool(request.values.get("all_messages"))
    if show_all_messages:
        limit = 10000
    else:
        limit = 10
    old_messages = get_latest_messages(limit)
    text = """
    <h1>Chat</h1>
    <form action="/chat/send" method="POST">
      <label for="content">Your Message: </label>
      <input type="text" id="content" name="content" autofocus />
      <input type="hidden" name="user_id" value="{user_id}" />
      <input type="hidden" name="all_messages" value="{show_all_messages}" />
      <input type="submit" value="send" />
    </form>
    <ul>
    """.format(user_id=user_id, show_all_messages=show_all_messages)
    for author, content in old_messages:
        text += "<li>{}: {}</li>\n".format(author, content)
    text += "</ul>"
    text += """
    <p><a href="{}">show all messages</a></p>
    """.format(url_for("chat_window", user_id=user_id, all_messages="true"))
    return text


@app.route("/chat/send", methods=["POST"])
def receive_new_message():
    user_id = request.values["user_id"]
    content = request.values["content"]
    store_message(user_id, content)
    return redirect(url_for("chat_window", user_id=user_id))


@app.route("/chat/admin/create")
def create_chat_databases():
    execute_sql(
        MySQL_DATABASE_CHAT_APP,
        """
        CREATE TABLE `users` (
            `UserId` INT(11) NOT NULL AUTO_INCREMENT,
            `UserName` VARCHAR(50) CHARACTER SET utf8mb4 NOT NULL,
            `Password` VARCHAR(21) NOT NULL,
            PRIMARY KEY (`UserId`),
            UNIQUE (`UserName`)
        );
        """
        )
    execute_sql(
        MySQL_DATABASE_CHAT_APP,
        """
        CREATE TABLE `messages` (
            `Messageid` INT(11) NOT NULL AUTO_INCREMENT,
            `SenderId` INT(11) NOT NULL,
            `MessageContent` VARCHAR(300) CHARACTER SET utf8mb4 NOT NULL,
            PRIMARY KEY (`MessageId`)
        );
        """
        )
    return "ok"


@app.route("/chat/admin/clear")
def clear_chat_databases():
    execute_sql(
        MySQL_DATABASE_CHAT_APP,
        """
        DROP TABLE `users`;
        """
        )
    execute_sql(
        MySQL_DATABASE_CHAT_APP,
        """
        DROP TABLE `messages`;
        """
        )
    return "ok"


def add_user(username, password):
    execute_sql(
        MySQL_DATABASE_CHAT_APP,
        "INSERT INTO `users` (`UserName`, `Password`) VALUES (%s, %s) ;",
        (username, password)
        )


def is_password_correct(username, password):
    # use username
    # skunk" ; DROP TABLE users ; SELECT * from users where UserName = "foo
    # to delete the users table
    # use password
    # " or ""="
    # to get access wihtout knowing the password
    if ALLOW_SQL_INJECTIONS:
        findings = execute_sql(
            MySQL_DATABASE_CHAT_APP,
            """SELECT `UserId` FROM `users` WHERE `UserName` = "{}" AND `Password` = "{}" ;""".format(username, password),
            None,
            True,
            )
        if findings:
            return True
        else:
            return False
    else:
        stored_password = execute_sql(
            MySQL_DATABASE_CHAT_APP,
            "SELECT `Password` FROM `users` WHERE `UserName` = %s ;",
            (username,)
            )
        if stored_password:
            return password == stored_password[0][0]
        else:
            return False


def get_user_id(username):
    try:
        if ALLOW_SQL_INJECTIONS:
            user_id = execute_sql(
                MySQL_DATABASE_CHAT_APP,
                """SELECT `UserId` FROM `users` WHERE `UserName` = "{}" ;""".format(username),
                None,
                True,
                )
        else:
            user_id = execute_sql(
                MySQL_DATABASE_CHAT_APP,
                "SELECT `UserId` FROM `users` WHERE `UserName` = %s ;",
                (username,)
                )
        if user_id:
            return user_id[0][0]
        else:
            return None
    except:
        return None


def store_message(userid, content):
    # destroy using message
    # foo" ) ;  DROP TABLE users ; INSERT INTO messages () VALUES (
    if ALLOW_SQL_INJECTIONS:
        execute_sql(
            MySQL_DATABASE_CHAT_APP,
            """
            INSERT INTO `messages` (`SenderId`, `MessageContent`) VALUES ("{}", "{}") ;
            """.format(userid, content),
            None,
            True,
            )
    else:
        execute_sql(
            MySQL_DATABASE_CHAT_APP,
            "INSERT INTO `messages` (`SenderId`, `MessageContent`) VALUES (%s, %s) ;",
            (userid, content),
            )



def get_latest_messages(number_of_messages=50):
    """
    Return given number of latest messages in the form of
    a list of tuples (name, message); the list is sorted by
    date of sending, first element is newest one.
    """
    # JOIN see https://www.w3schools.com/sql/sql_join.asp
    stuff = execute_sql(
        MySQL_DATABASE_CHAT_APP,
        """
        SELECT users.UserName, messages.MessageContent
        FROM messages INNER JOIN users
        ON users.UserId = messages.SenderId
        ORDER BY messages.MessageId DESC
        LIMIT %s
        ;
        """,
        (int(number_of_messages),)
        )
    return stuff



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