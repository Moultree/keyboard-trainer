import unittest
import sys
import os
from lib.game import Game
from lib.game import GameStats

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))


class TestGame(unittest.TestCase):
    def test_game_difficulty(self):
        game = Game()
        game.new(words_amount=20, difficulty="easy")
        self.assertEqual(game.difficulty, "easy")

        game.new(words_amount=20, difficulty="medium")
        self.assertEqual(game.difficulty, "medium")

        game.new(words_amount=20, difficulty="hard")
        self.assertEqual(game.difficulty, "hard")

    def test_stats_reset(self):
        stats = GameStats(words_amount=25)
        stats.accuracy = 80
        stats.bad_clicks = 1
        stats.good_clicks = 70
        stats.reset()
        self.assertEqual(stats.accuracy, 0)
        self.assertEqual(stats.bad_clicks, 0)
        self.assertEqual(stats.good_clicks, 0)

    def test_game_new(self):
        game = Game()
        words = game.words
        self.assertEqual(len(words), 20)
        self.assertIsInstance(words, list)
        self.assertIsInstance(words[0], str)

        game.new(30, "hard")
        new_words = game.words
        new_stats = game.stats
        self.assertIsInstance(new_words, list)
        self.assertIsInstance(new_words[0], str)
        self.assertEqual(new_stats.words_amount, 30)

    def test_game_words_provider(self):
        game = Game()
        words_provider = game.words_provider
        self.assertEqual(words_provider.easy_threshold, 5)
        self.assertEqual(words_provider.medium_threshold, 8)

        generated_words = words_provider.generate(10, "hard", theme=None)
        self.assertIsInstance(generated_words, list)
        self.assertEqual(len(generated_words), 10)
        self.assertIsInstance(generated_words[0], str)


if __name__ == "__main__":
    unittest.main()
