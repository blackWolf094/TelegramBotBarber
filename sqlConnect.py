import sqlite3

from pip._vendor.distlib import database

import main

class SQLConnect:

    def __init__(self, database_file):
        """Підключаємся до БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_order(self, user_id):
        """Стоврення нової записі"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'TelegramBot' ('spesialist, service, name, phone_number') VALUES (?,?,?,?)", (main.spesialist, main.service, main.name, main.phone_number))
