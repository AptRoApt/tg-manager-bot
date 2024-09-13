import sqlite3
from bot.utils.store.models import User

# Класс User для описания пользователя


# Класс Store для работы с базой данных
class Store:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT NOT NULL,
                    chat_id INTEGER NOT NULL
                )
            ''')

    def add_user(self, user: User):
        try:
            with self.connection:
                user.to_database()
                self.connection.execute('''
                    INSERT INTO users (id, username, first_name, chat_id) VALUES (?, ?, ?, ?)
                ''', (user.id, user.username, user.first_name, user.chat_id))
        except sqlite3.IntegrityError:
            self.update_user(user)

    def update_user(self, user):
        with self.connection:
            user.to_database()
            self.connection.execute('''
                UPDATE users SET username = ?, first_name= ?, chat_id = ?
                WHERE id = ?
            ''', (user.username, user.first_name, user.chat_id, user.id))

    def get_user_by_id(self, user_id) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute('''
                SELECT * FROM users WHERE id = ?
            ''', (user_id,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], username=row[1], first_name=row[2], chat_id=row[3])
        else:
            return None

    def get_user_by_username(self, username: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute('''
                        SELECT * FROM users WHERE username = ?
                    ''', (username.lower(),))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], username=row[1], first_name=row[2], chat_id=row[3])
        else:
            return None

    def delete_user(self, user_id):
        with self.connection:
            self.connection.execute('''
                DELETE FROM users WHERE id = ?
            ''', (user_id,))

    def close(self):
        self.connection.close()

