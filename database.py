import sqlite3


DATABASE_NAME = "online_shop.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    return connection


def get_db():
    connection = get_connection()

    print("1. Соединение открыто")

    try:
        yield connection
    finally:
        connection.close()
        print("3. Соединение закрыто")