import random


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    up_to = 0
    for c, w in choices:
        if up_to + w >= r:
            return c
        up_to += w
    assert False, "Shouldn't get here"