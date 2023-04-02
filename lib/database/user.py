from sqlite3 import Connection


class User:
    def __init__(
        self, conn: Connection, name: str, texts_typed: int, speed: int
    ) -> None:
        self.conn = conn
        self.name = name
        self.texts_typed = texts_typed
        self.speed = speed

    def history(self):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM user_history WHERE name=?;", (self.name,))
        return cursor.fetchall()

    def update(self, new_speed: int):
        self.speed = int(
            (self.speed * self.texts_typed + new_speed) / (self.texts_typed + 1)
        )
        self.texts_typed += 1

        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET texts_typed=?, speed=? WHERE name=?;",
            (self.texts_typed, self.speed, self.name),
        )
        cursor.execute(
            "INSERT INTO user_history (name, speed) VALUES (?, ?);",
            (self.name, new_speed),
        )
        self.conn.commit()
        cursor.close()

    def __repr__(self) -> str:
        return f"User(name = {self.name}, texts_typed = {self.texts_typed}, speed = {self.speed})"
