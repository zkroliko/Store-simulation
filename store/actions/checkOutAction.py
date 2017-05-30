import random

import numpy


class CheckOutAction:
    CONST_MIN_LENGTH = 5
    CONST_MAX_LENGTH = 30

    MIN_LENGTH_PER_ITEM = 0.25
    MAX_LENGTH_PER_ITEM = 5

    def __init__(self, client):
        self.client = client
        self.length = self.gen_time()
        self.time_left = self.length
        print("Client started checking out")

    def gen_time(self):
        time_const = random.randrange(self.CONST_MIN_LENGTH, self.CONST_MAX_LENGTH)
        items_count = sum(self.client.have.values())
        time_items = sum(numpy.random.uniform(self.MIN_LENGTH_PER_ITEM, self.MAX_LENGTH_PER_ITEM, items_count))
        return time_const+int(time_items)

    def ongoing(self):
        return self.time_left > 0

    def step(self):
        if self.ongoing():
            self.time_left -= 1
        else:
            self.finalize()

    def finalize(self):
        print("Client checking out at the exit after shopping for: {} turns".format(self.client.time_total))
        self.client.past_actions.append(self)
        self.client.action = None
        self.client.remove()
