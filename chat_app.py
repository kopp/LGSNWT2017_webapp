from flask import request, redirect, url_for
from sql_helpers import execute_sql

MySQL_DATABASE_CHAT_APP = "lgsnwt00$ChatApp"

ALLOW_SQL_INJECTIONS = True

def add_chat_app_to(app):
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
        show_all_messages = bool(request.values.get("all_messages"))
        return redirect(url_for("chat_window", user_id=user_id, all_messages=show_all_messages))


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
