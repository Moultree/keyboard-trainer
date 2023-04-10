from lib.words import WordList


class GameStats:
    def __init__(self, words_amount: int) -> None:
        self.words_amount = words_amount

        self.accuracy = 0
        self.good_clicks = 0
        self.bad_clicks = 0

    def reset(self):
        self.accuracy = 0
        self.good_clicks = 0
        self.bad_clicks = 0


class Game:
    def __init__(
        self, words_amount: int = 20, difficulty: str = "easy", theme: str = None
    ) -> None:
        self.words_amount = words_amount
        self.difficulty = difficulty
        self.theme = theme

        self.words_provider = WordList(easy_threshold=5, medium_threshold=8)
        self.words = self.words_provider.generate(
            self.words_amount, self.difficulty, theme
        )
        self.stats = GameStats(self.words_amount)

    def new(self, words_amount: int, difficulty: str, theme: str = None):
        self.words_amount = words_amount
        self.difficulty = difficulty
        self.theme = theme

        self.stats.reset()
        self.stats.words_amount = self.words_amount
        self.words = self.words_provider.generate(
            words_amount, difficulty, theme)
