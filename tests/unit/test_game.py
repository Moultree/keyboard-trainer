def test_game_difficulty(game):
    game.new(words_amount=20, difficulty="easy")
    assert game.difficulty == "easy"

    game.new(words_amount=20, difficulty="medium")
    assert game.difficulty == "medium"

    game.new(words_amount=20, difficulty="hard")
    assert game.difficulty == "hard"


def test_stats_reset(stats):
    stats.accuracy = 80
    stats.bad_clicks = 1
    stats.good_clicks = 70
    stats.reset()
    assert stats.accuracy == 0
    assert stats.bad_clicks == 0
    assert stats.good_clicks == 0


def test_game_new(game):
    words = game.words
    assert len(words) == 20
    assert isinstance(words, list)
    assert isinstance(words[0], str)

    game.new(30, "hard")
    new_words = game.words
    new_stats = game.stats
    assert isinstance(new_words, list)
    assert isinstance(new_words[0], str)
    assert new_stats.words_amount == 30


def test_game_words_provider(game):
    words_provider = game.words_provider
    assert words_provider.easy_threshold == 5
    assert words_provider.medium_threshold == 8

    generated_words = words_provider.generate(10, "hard")
    assert isinstance(generated_words, list)
    assert len(generated_words) == 10
    assert isinstance(generated_words[0], str)
