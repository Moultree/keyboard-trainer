import pytest

from os.path import join, dirname, abspath
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))


if True:
    from lib.words import WordList
    from lib.game import Game, Stats


@pytest.fixture(scope="module")
def game():
    game = Game()
    yield game


@pytest.fixture(scope="module")
def stats():
    game = Game()
    stats = Stats(game.words_amount)
    yield stats


@pytest.fixture(scope="module")
def word_list():
    word_list = WordList()
    yield word_list
