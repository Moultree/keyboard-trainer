import random
import os
import json
from nltk.corpus import wordnet

"""
word = input("Введите слово: ")

synonyms = []
for syn in wordnet.synsets(word):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())

synonyms = list(set(synonyms))

random.shuffle(synonyms)

print(synonyms[:1000])
"""


class WordList:
    words: list[str] = []

    def __init__(self, easy_threshold: int = 5, medium_threshold: int = 8) -> None:
        self.easy_threshold = easy_threshold
        self.medium_threshold = medium_threshold

    def get_words(self, theme: str):
        if theme is not None:
            temp = []
            for syn in wordnet.synsets(theme):
                for lemma in syn.lemmas():
                    word = lemma.name()
                    if word.isalpha():
                        temp.append(word)
            self.words = list(set(temp))
            if len(self.words) < 5:
                self.get_words(None)
        else:
            filename = "words.json"
            directory = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                data = json.load(file)

            self.words = [str(item["word"]).lower() for item in data["data"]]

    def sample(self, words_amount: int, threshold: callable, theme: str) -> list[str]:
        to_sample = [word for word in self.words if threshold(word)]
        if len(to_sample) < words_amount:
            self.get_words(theme)
            if theme is None:
                return self.sample(words_amount, threshold, theme)
        if theme is not None and len(to_sample) < words_amount:
            words_amount = len(to_sample)
        sampled = random.sample(to_sample, words_amount)

        for word in sampled:
            self.words.remove(word)

        return sampled

    def generate(self, words_amount: int, difficulty: str, theme: str) -> list[str]:
        if theme is not None:
            self.words.clear()
            self.sample(
                words_amount, lambda word: len(word) <= self.easy_threshold, theme
            )
        if not self.words:
            self.get_words(theme)

        match difficulty:
            case "easy":
                return self.sample(
                    words_amount, lambda word: len(word) <= self.easy_threshold, theme
                )
            case "medium":
                return self.sample(
                    words_amount,
                    lambda word: self.easy_threshold
                    < len(word)
                    <= self.medium_threshold,
                    theme,
                )
            case "hard":
                return self.sample(
                    words_amount, lambda word: self.medium_threshold < len(word), theme
                )
            case _:
                raise ValueError()
