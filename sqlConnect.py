import sqlite3

from pip._vendor.distlib import database

import main

def post_sql_query(sql_query):
    with sqlite3.connect('botDB.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Exception as e:
            pass
        result = cursor.fetchall()
        return result

# def register_user(user, username, first_name, last_name):
#     user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
#     user_check_data = post_sql_query(user_check_query)
#     if not user_check_data:
#         insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
#         post_sql_query(insert_to_db_query )

def register_user(spesialist, service, fullname, phone):
    insert_to_db_query = f'INSERT INTO TelegramBot (spesialist, service, name, phone_number) VALUES ({spesialist}, "{service}", "{fullname}", "{phone}");'
    post_sql_query(insert_to_db_query )

class SQLConnect:

    def __init__(self, database_file):
        """Підключаємся до БД"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_order(self, spesialist, service, fullname, phone):
        """Стоврення нової записі"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'TelegramBot' ('spesialist, service, name, phone_number') VALUES (?,?,?,?)", (main.spesialist, main.service, main.name, main.phone_number))
