import unittest
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from lib.database.db import Database
from lib.database.user import User


class TestDatabase(unittest.TestCase):
    def test_create_user(self):
        database = Database()
        user = database.create_user("Test User", 50)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.speed, 50)

    def test_create_duplicate_user(self):
        database = Database()
        user1 = database.create_user("Test User1", 50)
        user2 = database.create_user("Test User1", 60)
        self.assertEqual(user1.name, "Test User1")
        self.assertIsNone(user2)

    def test_get_user(self):
        database = Database()
        temp = database.create_user("Test User3", 50)
        user = database.get_user("Test User3")
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User3")
        self.assertEqual(user.speed, 50)

    def test_get_users(self):
        database = Database()
        users = database.get_users()
        self.assertGreater(len(users), 0)

    def test_user_history(self):
        database = Database()
        user = database.get_user("Test User")
        history = user.history()
        self.assertGreater(len(history), 0)

    def test_user_update(self):
        database = Database()
        user = database.get_user("Test User")
        self.assertIsNotNone(user)
        self.assertEqual(user.speed, 50)
        user.update(60)
        user = database.get_user("Test User")
        self.assertEqual(user.speed, 55)
