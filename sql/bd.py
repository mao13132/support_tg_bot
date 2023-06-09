import re
import sqlite3


class BotDB:
    def __init__(self, db_file):
        try:
            self.push_user_time = 24
            self.conn = sqlite3.connect(db_file, timeout=30)

            print()
            print(f'Успешно подключился к SQL базе данных "{db_file}"')

            self.cursor = self.conn.cursor()

            self.create_db()

        except Exception as es:
            print(f'SQL Ошибка при подключении к DB "{es}"')

    def create_db(self):
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_tg NIMERIC, "
                                f"name TEXT, "
                                f"full_name TEXT, "
                                f"login TEXT, "
                                f"language NIMERIC, "
                                f"email TEXT DEFAULT NULL, "
                                f"phone TEXT DEFAULT NULL, "
                                f"other TEXT DEFAULT NULL, "
                                f"push1 TEXT DEFAULT NULL, "
                                f"push2 TEXT DEFAULT NULL, "
                                f"join_date DATETIME, "
                                f"last_time DATETIME, "
                                f"rang TEXT DEFAULT new, "
                                f"license BOOLEAN DEFAULT 0, "
                                f"demo BOOLEAN DEFAULT 0, "
                                f"start_demo DATETIME, "
                                f"activ_client BOOLEAN DEFAULT 0)")

        except Exception as es:
            print(f'SQL исключение при создание таблицы users "{es}"')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"settings (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"keys TEXT, "
                                f"value NIMERIC DEFAULT 5)")

        except Exception as es:
            print(f'SQL исключение при создание таблицы settings "{es}"')



    def user_exist(self, user_id):
        # получаю id юзера в по его user_id в телеграме
        try:
            result = self.cursor.execute("SELECT id_tg FROM users WHERE id_tg = ?", (user_id,))
            response = result.fetchall()
        except Exception as es:
            print(f'SQL ошибка! При проверке пользователя в DB "{es}"')
            response = 'error'

        if response == []:
            return False

        return True

    def change_time(self, user_id, current_time):
        # добавляю юзера в БД f"UPDATE bigdata SET take3 = 1, seea = 0, min = {minimum}, max = {maximum} WHERE DATE = '{date}'")
        try:

            result = self.cursor.execute(f"UPDATE users SET last_time = '{current_time}' WHERE id_tg = '{user_id}'")
            self.conn.commit()
            x = result.fetchall()
        except Exception as es:
            print(f'Ошибка SQL: {es}')

    def add_user(self, id_tg, name, full_name, login, rang, times):
        # добавляю юзера в БД
        black = [' ', '?']
        for x in black:
            if x in login:
                login = str(login.replace(x, '_'))

        try:
            self.cursor.execute("INSERT OR IGNORE INTO users ('id_tg', "
                                "'name', "
                                "'full_name', "
                                "'login', "
                                "'join_date', "
                                "'last_time', "
                                "'rang', "
                                "'license', "
                                "'activ_client') VALUES (?,?,?,?,?,?,?,?,?)",
                                (id_tg, name, full_name, login, times, times, rang, 0, 0,))
            self.conn.commit()
        except Exception as es:
            print(f'SQL ошибка! Не смог добавить пользователя в DB "{es}"')

    def get_token(self):
        try:

            result = self.cursor.execute(f"SELECT value FROM settings "
                                         f"WHERE keys = 'token'")

            response = result.fetchall()

            if response == []:
                return []
            try:
                response = response[0][0]
            except:
                return False


            return response

        except Exception as es:
            print(f'Ошибка SQL get_ add_ads: {es}')
            return False

    def set_token(self, token):
        check_exist = self.get_token()

        if check_exist == []:
            try:
                self.cursor.execute("INSERT OR IGNORE INTO settings ('keys', 'value') VALUES (?,?)",
                                    ('token', token,))

                self.conn.commit()

                return True
            except Exception as es:
                print(f'SQL ошибка! Не смог добавить set_token в DB "{es}"')

                return False

        else:
            try:
                result = self.cursor.execute(f"UPDATE settings SET value = '{token}' WHERE keys = 'token'")
                self.conn.commit()

                return True
            except Exception as es:
                print(f'SQL ошибка! Не смог update set_token в DB "{es}"')
                return False

        return True

    def close(self):
        # Закрытие соединения
        self.conn.close()
