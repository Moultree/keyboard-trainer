from nicegui import ui


class Base:
    def __init__(self) -> None:
        ui.add_head_html("<link rel='stylesheet' href='/static/style.css' />")

        self.base = ui.column().classes("main")
