import random

import requests


class WordList:
    words: list[str] = []
    _URL = "https://www.randomwordgenerator.com/json/words.json"

    def __init__(self, easy_threshold: int = 5, medium_threshold: int = 8) -> None:
        self.easy_threshold = easy_threshold
        self.medium_threshold = medium_threshold

    def get_json(self):
        response = requests.get(self._URL)
        self.words = [item["word"] for item in response.json()["data"]]

    def sample(self, words_amount: int, threshold: callable) -> list[str]:
        to_sample = [word for word in self.words if threshold(word)]

        if len(to_sample) < words_amount:
            self.get_json()
            return self.sample(words_amount, threshold)

        sampled = random.sample(to_sample, words_amount)

        for word in sampled:
            self.words.remove(word)

        return sampled

    def generate(self, words_amount: int, difficulty: str) -> list[str]:
        if not self.words:
            self.get_json()

        if words_amount <= 0 or words_amount >= len(self.words):
            raise ValueError()

        match difficulty:
            case "easy":
                return self.sample(
                    words_amount, lambda word: len(word) <= self.easy_threshold
                )
            case "medium":
                return self.sample(
                    words_amount,
                    lambda word: self.easy_threshold
                    < len(word)
                    <= self.medium_threshold,
                )
            case "hard":
                return self.sample(
                    words_amount, lambda word: self.medium_threshold < len(
                        word)
                )
            case _:
                raise ValueError()
