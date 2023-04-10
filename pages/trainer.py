from string import ascii_lowercase

from nicegui import ui
from nicegui.events import KeyEventArguments
from lib.game import Game
from lib.database.db import Database
from .base import Base
import time


@ui.page("/trainer")
class Trainer(Base):
    def __init__(self) -> None:
        super().__init__()
        ui.keyboard(on_key=self.handle_input)

        self.words_wrapper = None

        self.game = Game(25)
        self.active = True
        self.measuring_time_is_started = False
        self.index = 0
        self.letters = []
        self.username = ""
        self.theme = ""
        self.build_ui()

    def update(self, words_amount: int, difficulty: str, theme: str = None):
        self.active = True
        self.index = 0
        self.letters = []
        self.measuring_time_is_started = False

        self.game.new(words_amount, difficulty, theme)
        self.update_stat()
        self.build_words()

    def build_words(self):
        self.words_wrapper.clear()
        self.words_wrapper.style("filter: none;")

        with self.words_wrapper:
            self.words_container = ui.element("div").classes("words")
            with self.words_container:
                for word in self.game.words:
                    with ui.element("div").classes("word"):
                        for letter in word.lower():
                            self.letters.append(
                                ui.label(letter).classes("letter"))
                    self.letters.append(ui.label(" ").classes("letter"))

        self.letters[0].classes("active")

        ui.update()

    def build_navbar(self, wrapper):
        with wrapper:
            with ui.row().classes("navbar") as navbar:
                ui.image("/static/logo.svg").classes("logo")
                with ui.row().classes("stats"):
                    self.mistakes_label = ui.label(
                        f"{self.game.stats.bad_clicks} mistakes"
                    )
                    self.accuracy_label = ui.label(
                        f"{self.game.stats.accuracy:.2f}% accuracy"
                    )

        return navbar

    def on_main_profile_button(self):
        if Base.username:
            ui.open("/profile")
        else:
            with ui.dialog().props("persistent").classes("dialog") as dialog, ui.card():
                dialog.open()
                ui.label("Pass the test once before use profile")
                with ui.row():
                    ui.button("Close", on_click=dialog.close)

    def save_button(self, dialog):
        self.update(self.game.words_amount, self.game.difficulty, self.theme)
        dialog.close()

    def set_theme(self):
        with ui.dialog().classes("dialog") as dialog, ui.card():
            dialog.open()
            with ui.row().classes("save"):
                ui.input(
                    placeholder="theme",
                    validation={
                        "Input too long": lambda value: len(value) < 20},
                ).bind_value(self, "theme")
                ui.button("Save", on_click=lambda: self.save_button(dialog)).classes(
                    "btn"
                )

    def build_buttons(self, wrapper):
        with wrapper:
            with ui.row().classes("toggles") as toggles:
                ui.button(
                    "RESTART",
                    on_click=lambda: self.update(
                        self.game.words_amount, self.game.difficulty
                    ),
                ).classes("btn restart")
                ui.button(
                    "PROFILE",
                    on_click=lambda: self.on_main_profile_button(),
                ).classes("btn")
                ui.button(
                    "THEME",
                    on_click=lambda: self.set_theme()).classes("btn")
                with ui.row():
                    ui.toggle(
                        [10, 25, 50, 75, 100],
                        value=self.game.words_amount,
                        on_change=lambda value: self.update(
                            value.value, self.game.difficulty
                        ),
                    ).classes("toggle")
                    ui.toggle(
                        ["Easy", "Medium", "Hard"],
                        value=self.game.difficulty.title(),
                        on_change=lambda value: self.update(
                            self.game.words_amount, value.value.lower()
                        ),
                    ).classes("toggle")

        return toggles

    def build_ui(self):
        with self.base:
            with ui.column().classes("trainer-main") as wrapper:
                self.navbar = self.build_navbar(wrapper)

                self.words_wrapper = ui.element("div").classes("text-wrapper")
                self.build_words()

                self.buttons = self.build_buttons(wrapper)

    def handle_input(self, event: KeyEventArguments):
        words_string = " ".join(self.game.words)
        if self.index == len(words_string):
            self.end_time = time.time()
            self.end_game()
            return

        if event.action.keydown and event.key.backspace:
            if self.index > 0 and words_string[self.index - 1] != " ":
                self.letters[self.index].classes(remove="bad good")
                self.index -= 1
                self.letters[self.index].classes(remove="bad good")
                self.letters[self.index + 1].classes(remove="active")
                self.letters[self.index].classes("active")
                return

        if str(event.key) not in (ascii_lowercase + " "):
            return

        if event.action.keydown:
            if self.index < len(words_string):
                if self.index == 1 and not self.measuring_time_is_started:
                    self.measuring_time_is_started = True
                    self.start_time = time.time()
                gl = words_string[self.index]
                letter = self.letters[self.index]

                if str(event.key) == gl:
                    letter.classes("good", remove="bad")
                    self.game.stats.good_clicks += 1
                else:
                    self.game.stats.bad_clicks += 1
                    letter.classes("bad", remove="good")
                self.index += 1
                self.letters[self.index - 1].classes(remove="active")
                self.letters[self.index].classes("active")
                self.game.stats.accuracy = (
                    self.game.stats.good_clicks
                    / (self.game.stats.good_clicks + self.game.stats.bad_clicks)
                    * 100
                )
        self.update_stat()

    def show_dialog(self, username):
        Base.username = username
        self.on_username_change(username)
        with ui.dialog().props("persistent").classes("dialog") as dialog, ui.card():
            dialog.open()
            ui.label("Your quiz statistics have been saved.")
            ui.label("What would you like to do next?")
            with ui.row():
                ui.button("Profile", on_click=lambda: ui.open("/profile"))
                ui.button("Continue", on_click=lambda: ui.open("/trainer"))

    def on_username_change(self, username: str):
        if not username:
            return

        speed = int(self.game.words_amount /
                    ((self.end_time - self.start_time) / 60))
        if not self.db.create_user(username, speed):
            user = self.db.get_user(username)
            user.update(speed)
            ui.notify("Saved")

    def end_game(self):
        if not self.active:
            return

        with self.navbar:
            self.navbar.clear()
            with ui.row():
                ui.image("/static/logo.svg").classes("logo")
                ui.label("Your stats:").style("font-size: 36px;")

        self.words_container.style("filter: blur(10px);")

        with self.words_wrapper:
            with ui.column().classes("endgame"):
                ui.label(f"Accuracy: {self.game.stats.accuracy:.2f}%")
                ui.label(f"Mistakes: {self.game.stats.bad_clicks}")
                ui.label(
                    f"Wpm: {int(self.game.words_amount/((self.end_time - self.start_time)/60))}"
                )

        with self.buttons:
            self.buttons.clear()
            ui.button("RESTART", on_click=lambda: ui.open("/trainer")).classes(
                "btn restart"
            )
            with ui.row().classes("save"):
                ui.input(
                    placeholder="username",
                    validation={
                        "Input too long": lambda value: len(value) < 20},
                ).bind_value(self, "username")
                ui.button(
                    "Save", on_click=lambda: self.show_dialog(self.username)
                ).classes("btn")

        self.active = False

    def update_stat(self):
        self.accuracy_label.set_text(
            f"{self.game.stats.accuracy:.2f}% accuracy")
        self.mistakes_label.set_text(f"{self.game.stats.bad_clicks} mistakes")
        ui.update()
