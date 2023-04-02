from nicegui import ui
from lib.database.db import Database


class Base:
    username = ""

    def __init__(self) -> None:
        ui.colors(primary="#8A7A73", secondary="#FFFFFF")
        ui.add_head_html("<link rel='stylesheet' href='/static/style.css' />")

        self.base = ui.column().classes("main")
        self.db = Database()
