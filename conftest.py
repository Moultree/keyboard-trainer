from lib.database.user import User
from lib.database.db import Database
from lib.game import Game, GameStats
from lib.words import WordList
import pytest

from os.path import join, dirname, abspath
import sys
import sqlite3

sys.path.append(abspath(join(dirname(__file__), "..")))


@pytest.fixture(scope="module")
def database():
    db = Database()

    yield db


@pytest.fixture(scope="module")
def user(database):
    user = database.create_user("test_user", 50)
    yield user

    cursor = database.conn.cursor()
    cursor.execute("DELETE FROM users WHERE name=?", (user.name,))
    cursor.execute("DELETE FROM user_history WHERE name=?", (user.name,))
    database.conn.commit()
    cursor.close()


@pytest.fixture(scope="module")
def game():
    game = Game()
    yield game


@pytest.fixture(scope="module")
def stats():
    game = Game()
    stats = GameStats(game.words_amount)
    yield stats


@pytest.fixture(scope="module")
def word_list():
    word_list = WordList()
    yield word_list
