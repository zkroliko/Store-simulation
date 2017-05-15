import itertools


def places_to_move(x, y, limit_x, limit_y):
    return list(set(places_to_be(x, y, limit_x, limit_y)) - {(x, y)})


def places_to_be(x, y, limit_x, limit_y):
    dx = [x - 1, x, x + 1]
    dy = [y - 1, y, y + 1]
    return [(x, y) for x, y in itertools.product(dx, dy) if limit_x > x >= 0 and limit_y > y >= 0]


