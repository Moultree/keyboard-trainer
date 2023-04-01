from nicegui import ui
from .base import Base


@ui.page("/profile")
class Profile(Base):
    def __init__(self) -> None:
        super().__init__()

        self.username = ""
        self.texts_typed = 0
        self.typing_speed = 0

        self.build_ui()

    def build_ui(self):
        with self.base:
            with ui.row():
                ui.image("/static/logo.svg").classes("logo")
