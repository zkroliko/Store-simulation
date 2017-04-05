import random


class PickAction:
    MIN_PICK_LENGTH = 2
    MAX_PICK_LENGTH = 8

    def __init__(self, client, shelf):
        self.client = client
        self.item = shelf.category
        self.time_left = random.randrange(self.MIN_PICK_LENGTH, self.MAX_PICK_LENGTH)

    def ongoing(self):
        return self.time_left > 0

    def step(self):
        if self.ongoing():
            self.time_left -= 1
        else:
            self.finalize()

    def finalize(self):
        print("Client picked up an item of category {}".format(self.item))
        self.client.need[self.item] -= 1
        self.client.have[self.item] += 1
        self.client.picking = None
