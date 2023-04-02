from nicegui import ui
from .base import Base
from matplotlib import pyplot as plt
import matplotlib as mpl


@ui.page("/profile")
class Profile(Base):
    def __init__(self) -> None:
        super().__init__()
        self.username = Base.username
        try:
            self.user = self.db.get_user(self.username)
        except AttributeError:
            pass
        self.build_ui()

    def build_ui(self):
        with self.base:
            with ui.row().classes("statisticlabel"):
                ui.label("your results:")
            with ui.row().classes("profilestats"):
                with ui.column():
                    ui.label("your name").classes("legenda")
                    ui.label(f"{self.user.name}")
                with ui.column():
                    ui.label("total texts typed").classes("legenda")
                    ui.label(f"{self.user.texts_typed}")
                with ui.column():
                    ui.label("your avg wpm").classes("legenda")
                    ui.label(f"{self.user.speed}")

            history = self.user.history()
            plt.style.use("dark_background")
            with ui.row().classes("graphiclabel"):
                ui.label("wpm history")
            with ui.pyplot():
                plt.plot(range(len(history)), [text[1] for text in history], "-")
