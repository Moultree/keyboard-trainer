def test_create_user(database):
    user = database.create_user("Test User", 50)
    assert user is not None
    assert user.name == "Test User"
    assert user.speed == 50


def test_create_duplicate_user(database):
    user1 = database.create_user("Test User", 50)
    user2 = database.create_user("Test User", 60)
    assert user1 is None
    assert user2 is None


def test_get_user(database):
    user = database.get_user("Test User")
    assert user is not None
    assert user.name == "Test User"
    assert user.speed == 50


def test_get_users(database):
    users = database.get_users()
    assert len(users) > 0


def test_user_history(database):
    user = database.get_user("Test User")
    history = user.history()
    assert len(history) > 0


def test_user_update(database):
    user = database.get_user("Test User")
    assert user is not None
    assert user.speed == 50
    user.update(60)
    user = database.get_user("Test User")
    assert user.speed == 55
