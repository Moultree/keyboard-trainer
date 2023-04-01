from nicegui import app, ui

from pages.home import Home
from pages.trainer import Trainer

app.add_static_files("/static", "static")

ui.run(title="Typing Trainer", favicon="static/logo.svg", dark=True)
