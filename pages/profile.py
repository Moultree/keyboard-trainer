from nicegui import ui
from .base import Base
from lib.database.db import Database
from .trainer import Trainer


@ui.page("/profile")
class Profile(Base):
    def __init__(self) -> None:
        super().__init__()
        self.username = Base.username
        self.user = self.db.get_user(self.username)
        self.build_ui()

    def build_ui(self):
        with ui.row().classes("profilestats"):
            ui.label(f"{self.user.name}")
            ui.label(f"{self.user.texts_typed}")
            ui.label(f"{self.user.speed}")
