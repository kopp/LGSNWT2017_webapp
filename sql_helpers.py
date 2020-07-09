import mysql.connector

import sys



MySQL_HOST = "lgsnwt00.mysql.pythonanywhere-services.com"

MySQL_USER = "lgsnwt00"

MySQL_PASSWORD = "foobarasdf"



# SQL helpers



# See

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

# for how to "talk" to a MySQL database using Python.

# See

# https://stackoverflow.com/a/1482477/2165903

# for information on "weak references"



def _run_single_sql_statement(cursor, sql_code, data):

    cursor.execute(sql_code, data, multi=False)

    results = []

    for result in cursor:

        results.append(result)

    return results



def _run_multiple_sql_statements(cursor, sql_code, data):

    iterator = cursor.execute(sql_code, data, multi=True)

    results = []

    for sql_result in iterator:

        for result in sql_result:

            results.append(result)

    return results





def execute_sql(database, code, data=None, multiple=False):
    """Execute code, return a list of results.

    :param code str: sql query to run.
        You may include %s or %(name)s which will get replaced by the respective
        element in ``data``.

    :param data: Either a tuple with one value per %s in ``code`` -- IMPORTANT:
        To create a tuple with only one value, use ``(foo,)`` instead of just
        ``(foo)`` -- or a dictionary with ``name: value`` for each name in
        ``%(name)s`` in ``code``.

    :param multiple boolen: Run multiple SQL statements -- EXPERIMENTAL

    https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    """

    connection = mysql.connector.connect(
        host=MySQL_HOST,
        user=MySQL_USER,
        passwd=MySQL_PASSWORD,
        database=database,
        charset="utf8mb4",
        collation="utf8mb4_general_ci",
    )

    cursor = connection.cursor()
    try:
        if not multiple:
            results = _run_single_sql_statement(cursor, code, data)
        else:
            results = _run_multiple_sql_statements(cursor, code, data)

        connection.commit()  # make sure, data is committed to the DB
        # do this after reading results from cursor, otherwise you get
        #    InternalError("Unread result found")
        cursor.close()

        connection.close()
    except:
        raise ValueError("Error {} while executing SQL Query {}".format(
            sys.exc_info(),
            cursor.statement,
            ))

    return results