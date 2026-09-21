from graham_scan import next_point


def test_next_point():
    points = [(1, 10), (2, 9), (2, 8), (3, 8)]
    assert next_point(stack=[0, 1], points=points, current_point=1) == ([0, 1, 2], 2)
    assert next_point(stack=[0, 1, 2], points=points, current_point=2) == ([0, 1], 2)


def test_next_point2():
    points = [(260, 315), (488, 242), (281, 166), (214, 255), (128, 163)]
    assert next_point(stack=[0, 1, 2], points=points, current_point=3) == (
        [0, 1, 2, 4],
        4,
    )
