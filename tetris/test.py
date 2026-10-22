from tetromino import centered, mesure, most_connections


def test_centered():
    tetromino_I = ((0, 1), (1, 1), (2, 1), (3, 1))
    tetromino_S = ((1, 0), (1, 1), (2, 1), (2, 2))
    assert centered(tetromino_I) == True
    assert centered(tetromino_S) == True


def test_mesure():
    tetromino_2 = ((1, 1), (1, 2), (2, 1), (2, 2))
    tetromino_3 = ((0, 1), (1, 1), (1, 2), (1, 3))
    tetromino_4 = ((3, 0), (3, 1), (3, 2), (3, 3))
    assert mesure(tetromino_2) == 2
    assert mesure(tetromino_3) == 3
    assert mesure(tetromino_4) == 4


def test_most_connections():
    tetromino_S = ((1, 0), (1, 1), (2, 1), (2, 2))
    assert most_connections(tetromino_S) == (1, 1)
