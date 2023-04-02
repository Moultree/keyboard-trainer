from sqlite3 import Connection


class User:
    def __init__(
        self, conn: Connection, name: str, texts_typed: int, speed: int
    ) -> None:
        self.conn = conn
        self.name = name
        self.texts_typed = texts_typed
        self.speed = speed

    def update(self, new_speed: int):
        self.texts_typed += 1
        self.speed = int((self.speed + new_speed) / self.texts_typed)

        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET texts_typed=?, speed=? WHERE name=?;",
            (self.texts_typed, self.speed, self.name),
        )
        self.conn.commit()
        cursor.close()

    def __repr__(self) -> str:
        return f"User(name = {self.name}, texts_typed = {self.texts_typed}, speed = {self.speed})"
