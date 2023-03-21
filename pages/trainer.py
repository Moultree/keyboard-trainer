from string import ascii_lowercase

from nicegui import ui
from nicegui.events import KeyEventArguments

from lib.game import Game

from .base import Base


@ui.page("/trainer")
class Trainer(Base):
    def __init__(self) -> None:
        super().__init__()
        ui.keyboard(on_key=self.handle_input)

        self.words_wrapper = None

        self.game = Game(25)

        self.index = 0
        self.letters = []

        self.build_ui()

    def update(self, words_amount: int, difficulty: str):
        self.index = 0
        self.letters = []

        self.game.new(words_amount, difficulty)
        self.update_stat()
        self.build_words()

    def build_words(self):
        self.words_wrapper.clear()

        with self.words_wrapper:
            with ui.element("div").classes("words"):
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
            with ui.row().classes("navbar"):
                ui.image("/static/logo.svg").classes("logo")
                with ui.row().classes("stats"):
                    self.words_label = ui.label(
                        f"{self.game.stats.words_printed}/{self.game.stats.words_amount} words"
                    )
                    self.accuracy_label = ui.label(
                        f"{self.game.stats.accuracy:.2f}% accuracy"
                    )

    def build_buttons(self, wrapper):
        with wrapper:
            with ui.row().classes("toggles"):
                ui.button(
                    "RESTART",
                    on_click=self.update(
                        self.game.words_amount, self.game.difficulty),
                ).classes("btn restart")
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

    def build_ui(self):
        with self.base:
            with ui.column().classes("trainer-main") as wrapper:
                self.build_navbar(wrapper)

                self.words_wrapper = ui.element("div").classes("text-wrapper")
                self.build_words()

                self.build_buttons(wrapper)

    def handle_input(self, event: KeyEventArguments):
        words_string = " ".join(self.game.words)
        if self.index == len(words_string):
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
            self.game.stats.clicks += 1
            if self.index < len(words_string):
                gl = words_string[self.index]
                letter = self.letters[self.index]

                if str(event.key) == gl:
                    if str(event.key) == " " or (self.index + 1) == len(words_string):
                        self.game.stats.words_printed += 1
                    letter.classes("good", remove="bad")
                    self.game.stats.good_clicks += 1
                else:
                    letter.classes("bad", remove="good")
                self.index += 1
                self.letters[self.index - 1].classes(remove="active")
                self.letters[self.index].classes("active")
                self.game.stats.accuracy = (
                    self.game.stats.good_clicks / self.game.stats.clicks * 100
                )
        self.update_stat()

    def update_stat(self):
        self.accuracy_label.set_text(
            f"{self.game.stats.accuracy:.2f}% accuracy")
        if self.game.stats.words_printed <= self.game.words_amount:
            self.words_label.set_text(
                f"{self.game.stats.words_printed}/{self.game.words_amount} words"
            )
        ui.update()
