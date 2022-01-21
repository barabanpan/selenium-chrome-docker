import sqlite3

CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS chat_table (
        chat_id INT PRIMARY KEY
    )
"""

SELECT_ALL_QUERY = """
    SELECT chat_id from chat_table
"""

INSERT_ONE_QUERY = """
    INSERT INTO chat_table (chat_id)
    VALUES (%s)
"""


def execute_query(query):
    try:
        sqlite_connection = sqlite3.connect('sqlite.db')
        cursor = sqlite_connection.cursor()
    
        cursor.execute(query)
        result = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting:", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()


def add_id(chat_id):
    # print("q - ", INSERT_ONE_QUERY % chat_id)
    a = execute_query(INSERT_ONE_QUERY % chat_id)
    # print("res of insert - ", a)


def get_all_ids():
    return execute_query(SELECT_ALL_QUERY)


execute_query(CREATE_QUERY)

