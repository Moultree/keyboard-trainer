import sqlite3
from .user import User


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("users.db")

        self.create_table()
        self.names = [user.name for user in self.get_users()]

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(name text NOT NULL, texts_typed integer, speed integer);"
        )
        self.conn.commit()
        cursor.close()

    def get_user(self, name: str) -> User:
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users WHERE name=?;", (name, ))
        fetched = cursor.fetchone()
        return User(self.conn, fetched[0], fetched[1], fetched[2]) if fetched else None

    def get_users(self) -> list[User]:
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users;")
        return [User(self.conn, item[0], item[1], item[2]) for item in cursor.fetchall()]

    def create_user(self, name: str, speed: int) -> User:
        if name in self.names:
            return None

        user = User(self.conn, name, speed, 1)

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?);",
            (user.name, user.texts_typed, user.speed)
        )
        self.conn.commit()
        cursor.close()

        self.names.append(user.name)

        return user


"""
page:
    db = Database

    on_gameover():
        name = input()
        if not db.create_user(name, speed):
            user = db.get_user(user)
            user.update_speed(speed)
"""
