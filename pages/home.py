from nicegui import ui

from .base import Base


@ui.page("/")
class Home(Base):
    def __init__(self) -> None:
        super().__init__()

        with self.base:
            with ui.row():
                ui.image("/static/logo.svg").classes("logo")
                ui.label("Typing Trainer").classes("name")
            ui.button("Start", on_click=lambda: ui.open(
                "/trainer")).classes("btn")
